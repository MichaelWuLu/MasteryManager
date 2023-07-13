import PySimpleGUI as sg
import json
import os
from PIL import Image, ImageTk, ImagePath
from get_assets import get_summoner_icon, get_champion_square
from riot_api import get_by_summoner_name, get_mastery_by_summoner_id, get_value_from_json, get_mastery_score_by_calculation


Icon_size = 64, 64
champion_square_size = 50, 50


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


def load_data_from_json(wanted_data):
    if wanted_data == ('summoner_data'):
        # Load summonerName.json and mastery.json
        with open('temp/summonerName.json') as file:
            summoner_data = json.load(file)
        return summoner_data

    if wanted_data == ('mastery_data'):
        with open('temp/mastery.json') as file:
            mastery_data = json.load(file)
            mastery_data = sorted(mastery_data, key=lambda k: (k['championLevel'], k['championPoints']), 
                                  reverse=True)
        return mastery_data


def create_layout():
    global Icon_size
    global champion_square_size
    # Create GUI layout for PySimpleGUI
    summoner_data = load_data_from_json('summoner_data')
    mastery_data = load_data_from_json('mastery_data')

    input_layout = [
        [sg.Input(size=(15, 1), key='-INPUT-'), # Input field
         sg.Button('', key='-SUBMIT-', 
                   image_source='MasterieManager/MasteryManager/images/magnifying_glass_icon.png', 
                   image_size=(25, 25), tooltip="Finding new Summoner"), # Submit button
         sg.Button('', key='-UPDATE-', 
                   image_source='MasterieManager/MasteryManager/images/refresh_icon.png', 
                   image_size=(25, 25), tooltip="Update current summoner") # Update button
         ]]

    layout = [ 
        [   # Header, containing summoner name, mastery score and input field with buttons
            sg.Image(size=(Icon_size), key='-ICON-'),
            sg.Column([[
                (sg.Text(summoner_data['name'], font=('Helvetica', 20)) 
                if i == 0 else sg.Text(f"Mastery lvl: {get_mastery_score_by_calculation()}"))
            ] for i in range(2)], key='-SUMMONER-'),
            sg.Column(input_layout, element_justification='right', expand_x=True)
        ],
        [   # Body, containing all champion mastery data
            sg.Column([[
                sg.Image(size=champion_square_size, key=f'-CHAMPION-{champ["championId"]}-'),
                sg.Text(f'Name', font=('Helvetica', 12)),
                sg.Text(f'Level: {champ["championLevel"]}', font=('Helvetica', 12)),
                sg.Text(f'Points: {champ["championPoints"]}', font=('Helvetica', 12)),
            ] for champ in mastery_data], scrollable=True, size=(400, 600), key='-MASTERY-')
        ]
    ]

    return layout


def update_window():
    # Create/Update window with new layout
    layout = create_layout()
    window = sg.Window('Mastery Manager', layout, finalize=True)
    return window


def update_icon(window):
    global Icon_size
    # Update summoner icon
    summoner_data = load_data_from_json('summoner_data')
    summoner_icon = Image.open(f'temp/icons/icon{summoner_data["profileIconId"]}.jpg')
    summoner_icon = summoner_icon.resize(Icon_size)
    summoner_icon = ImageTk.PhotoImage(summoner_icon)
    window['-ICON-'].update(data=summoner_icon)


def update_champion_squares(window):
    global champion_square_size
    # Update champion squares
    mastery_data = load_data_from_json('mastery_data')
    for champ in mastery_data:
        champion_square = Image.open(f'temp/champions/champ{champ["championId"]}.jpg')
        champion_square = champion_square.resize(champion_square_size)
        champion_square = ImageTk.PhotoImage(champion_square)
        window[f'-CHAMPION-{champ["championId"]}-'].update(data=champion_square)


def run_app():
    # Run the app
    # Create window with layout from the create_layout() function
    window = update_window()

    # Load summoner icon in Header
    update_icon(window)

    # Load champion squares in Body
    update_champion_squares(window)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            # End loop and close window
            break
        elif event == '-SUBMIT-':
            # Get all assets and update window
            get_all_assets(values['-INPUT-'])
            window.close()
            window = update_window()
            update_icon(window)
            update_champion_squares(window)
        elif event == '-UPDATE-':
            # Update window with potential new assets
            summoner_data = load_data_from_json('summoner_data')
            get_all_assets(summoner_data['name'])
            window.close()
            window = update_window()
            update_icon(window)
            update_champion_squares(window)

    window.close()
    

if __name__ == "__main__":
    run_app()
