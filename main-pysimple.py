import PySimpleGUI as sg
import json
import os
from get_assets import get_summoner_icon, get_champion_square
from riot_api import get_by_summoner_name, get_mastery_by_summoner_id, get_value_from_json, get_mastery_score_by_calculation


def get_all_assets(summonerName):
    # Get summonerName.json containing the correct summoners information
    if not os.path.exists('temp/summonerName.json'):
        get_by_summoner_name(summonerName)
    else:
        with open('temp/summonerName.json') as file:
            summoner_data = json.load(file)
        if summoner_data['name'] != summonerName:
            get_by_summoner_name(summonerName)

    # Get summoner icon if it doesn't exist
    profileIconId = get_value_from_json('temp/summonerName.json', 'profileIconId')
    if not os.path.exists(f'temp/icons/icon{profileIconId}.jpg'):
        get_summoner_icon(profileIconId)
    
    # Get/Update mastery.json containing the summoners mastery information
    get_mastery_by_summoner_id()
    # Get champion squares if they don't exist
    with open('temp/mastery.json') as file:
        mastery_data = json.load(file)
    for champ in mastery_data:
        if not os.path.exists(f"temp/champions/champ{champ['championId']}.jpg"):
            get_champion_square(champ['championId'])


def load_data_from_json():
    # Load summonerName.json and mastery.json
    with open('temp/summonerName.json') as file:
        summoner_data = json.load(file)

    with open('temp/mastery.json') as file:
        mastery_data = json.load(file)
        mastery_data = sorted(mastery_data, key=lambda k: (k['championLevel'], k['championPoints']), reverse=True)

    return summoner_data, mastery_data


def create_layout():
    # Create GUI layout for PySimpleGUI
    summoner_data, mastery_data = load_data_from_json()

    input_layout = [
        [sg.Input(size=(15, 1), key='-INPUT-'), # Input field
         sg.Button('[?]', key='-SUBMIT-'), # Submit button
         sg.Button('Updt', key='-UPDATE-') # Update button
         ]]

    layout = [ 
        [   # Header, containing summoner name, mastery score and input field with buttons
            sg.Column([[
                (sg.Text(summoner_data['name'], font=('Helvetica', 20)) if i == 0 else sg.Text(get_mastery_score_by_calculation()))
            ] for i in range(2)], key='-SUMMONER-'),
            sg.Column(input_layout, element_justification='right', expand_x=True)
        ],
        [   # Body, containing all champion mastery data
            sg.Column([[
                sg.Text(f'ID: {item["championId"]}, Level: {item["championLevel"]}, Points: {item["championPoints"]}', font=('Helvetica', 12))
            ] for item in mastery_data], scrollable=True, size=(400, 600), key='-MASTERY-')
        ]
    ]

    return layout


def update_window():
    # Create/Update window with new layout
    layout = create_layout()
    window = sg.Window('Mastery Manager', layout)
    return window


def run_app():
    # Run the app
    # Fetch json data
    summoner_data, mastery_data = load_data_from_json()
    
    # Create window
    window = update_window()

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            # Close window
            break
        elif event == '-SUBMIT-':
            # Get all assets and update window
            get_all_assets(values['-INPUT-'])
            window.close()
            window = update_window()
        elif event == '-UPDATE-':
            # Update window with potential new assets
            get_all_assets(summoner_data['name'])
            window.close()
            window = update_window()

    window.close()
    

if __name__ == "__main__":
    run_app()
