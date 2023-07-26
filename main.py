import PySimpleGUI as sg
import json
import os
from PIL import Image, ImageTk
from get_assets import get_summoner_icon, get_champion_square
from riot_api import get_by_summoner_name, get_mastery_by_summoner_id, get_value_from_json, get_mastery_score_by_calculation

Icon_size = 64, 64
champion_square_size = 50, 50
version = 'v1.1'


def get_all_assets(summonerName):
    # Get summonerName.json containing the correct summoners information
    if not os.path.exists('MasteryManager/temp/summonerName.json'):
        get_by_summoner_name(summonerName)
    else:
        with open('MasteryManager/temp/summonerName.json') as file:
            summoner_data = json.load(file)
        if summoner_data['name'] != summonerName:
            get_by_summoner_name(summonerName)

    # Get summoner icon if it doesn't exist
    profileIconId = get_value_from_json('MasteryManager/temp/summonerName.json', 'profileIconId')
    if not os.path.exists(f'MasteryManager/temp/icons/icon{profileIconId}.jpg'):
        get_summoner_icon(profileIconId)
    
    # Get/Update mastery.json containing the summoners mastery information
    get_mastery_by_summoner_id()
    # Get champion squares if they don't exist
    with open('MasteryManager/temp/mastery.json') as file:
        mastery_data = json.load(file)

    for champ in mastery_data:
        if not os.path.exists(f"MasteryManager/temp/champions/champ{champ['championId']}.jpg"):
            get_champion_square(champ['championId'])


def load_data_from_json(wanted_data):
    if wanted_data == ('summoner_data') and os.path.exists('MasteryManager/temp/summonerName.json'):
        # Load summonerName.json and mastery.json
        with open('MasteryManager/temp/summonerName.json') as file:
            summoner_data = json.load(file)
        return summoner_data
    elif wanted_data == ('summoner_data'):
        summoner_data = {
            'name': 'SummonerName', 
            'profileIconId': 0
            }
        return summoner_data

    if wanted_data == ('mastery_data') and os.path.exists('MasteryManager/temp/mastery.json'):
        with open('MasteryManager/temp/mastery.json') as file:
            mastery_data = json.load(file)

            # temporary filter for displaying mastery level 4 and blow first
            #for champ in mastery_data:
             #   if champ['championLevel'] > 4:
              #      champ['championLevel'] = 0

            mastery_data = sorted(mastery_data, key=lambda k: (k['championLevel'], k['championPoints']), 
                                  reverse=True)
        return mastery_data
    
    elif wanted_data == ('mastery_data'):
        mastery_data = [
            {'championId': 0, 
             'championName': 'No mastery data found',
             'championLevel': 0,
             'championPoints': 0
            }
        ]
        return mastery_data


def create_layout(mastery_data=None, version=version):
    global Icon_size
    global champion_square_size
    # Create GUI layout for PySimpleGUI
    summoner_data = load_data_from_json('summoner_data')
    champion_data = load_data_from_json('champion_data')
    if not mastery_data:
        mastery_data = load_data_from_json('mastery_data')

    input_layout = [
        [sg.Input(size=(15, 1), key='-INPUT-'), # Input field
         sg.Button('', key='-SUBMIT-', 
                   image_source='MasteryManager/images/magnifying_glass_icon.png', 
                   image_size=(25, 25), tooltip="Finding new Summoner", bind_return_key=True), # Submit button
         sg.Button('', key='-UPDATE-', 
                   image_source='MasteryManager/images/refresh_icon.png', 
                   image_size=(25, 25), tooltip="Update current summoner") # Update button
         ]]

    layout = []

    header = [   # Header, containing summoner name, mastery score and input field with buttons
        sg.Image(size=(Icon_size), key='-ICON-'),
        sg.Column([
            [
            (sg.Text(summoner_data['name'], font=('Helvetica', 15), key='-SUMMONER NAME-', auto_size_text=True) if i == 0 
                else sg.Text(f"Mastery lvl: {get_mastery_score_by_calculation()}", key='-MASTERY-SCOERE-')) 
        ] for i in range(2)], key='-SUMMONER-'),
        sg.Column(input_layout, element_justification='right', expand_x=True)
    ]
    
    filters_and_sort = [
        [
            sg.Combo(['Remove lv 7', 'Remove lv >5', 'Remove lv >4'], default_value='Filter', enable_events=True, key='-FILTER-', readonly=True),
            sg.Combo(['By level, highest first', 'By level, lowest first', 'By points, highest first', 'By points, lowest first'], default_value='Sort', enable_events=True, key='-SORT-', readonly=True),
            sg.Button('Clear filters', key='-CLEAR-')
        ],
        [
            sg.Text('Search for champ by name:', font=('Helvetica', 12), key='-FILTER-TEXT-'),
            sg.Input(size=(25, 1), key='-FILTER-INPUT-', enable_events=True),
        ]
    ]
    
    body_v_1_0 = [   # Body, containing all champion mastery data
        sg.Column([
            [
            sg.Image(size=champion_square_size, key=f'-CHAMPION-{int(champ["championId"])}-IMAGE-'),
            sg.Text(str(champ['championName']), font=('Helvetica', 12), key=f'-CHAMPION-{int(champ["championId"])}-NAME-'),
            sg.Text(f'Level: {str(champ["championLevel"])}', font=('Helvetica', 12), key=f'-CHAMPION-{int(champ["championId"])}-LEVEL-'),
            sg.Text(f'Points: {str(champ["championPoints"])}', font=('Helvetica', 12), key=f'-CHAMPION-{int(champ["championId"])}-POINTS-')
        ] for champ in mastery_data], scrollable=True, vertical_scroll_only=True, key='-MASTERY-', expand_x=True, size=(None, 500))
    ]
    """
    champion_data = load_data_from_json('mastery_data')

    champion_list = []
    for champ in champion_data:
        x = [
                sg.Image(size=champion_square_size, key=f'-CHAMPION-{int(champ["championId"])}-IMAGE-', visible=False),
                sg.Text(str(champ['championName']), font=('Helvetica', 12), key=f'-CHAMPION-{int(champ["championId"])}-NAME-', visible=False),
                sg.Text(f'Level: ', font=('Helvetica', 12), key=f'-CHAMPION-{int(champ["championId"])}-LEVEL-', visible=False),
                sg.Text(f'Points: ', font=('Helvetica', 12), key=f'-CHAMPION-{int(champ["championId"])}-POINTS-', visible=False)
            ]
        champion_list.append(x)

    body_v_1_2 = [   # Body, containing all champion mastery data
        sg.Button('Testing', key='-TEST-'),
        sg.Column([champion_list],scrollable=True),
        sg.Text('Test')
    ]"""

    layout.append(header)
    layout.append(filters_and_sort)
    if version == 'v1.1':
        layout.append(body_v_1_0)
        
    #elif version == 'v1.2':
     #   layout.append(body_v_1_2)


    return layout


def update_column(mastery_data):
    # Update the column containing all champion mastery data
    layout = sg.Column([
                [
                sg.Image(size=champion_square_size, key=f'-CHAMPION-{champ["championId"]}-'),
                sg.Text(champ['championName'], font=('Helvetica', 12)),
                sg.Text(f'Level: {champ["championLevel"]}', font=('Helvetica', 12)),
                sg.Text(f'Points: {champ["championPoints"]}', font=('Helvetica', 12))
            ] for champ in mastery_data], scrollable=True, vertical_scroll_only=True, key='-MASTERY-', expand_x=True, size=(None, 500))
    
    return layout


def update_window(mastery_data=None):
    # Create/Update window with new layout
    if mastery_data:
        layout = create_layout(mastery_data)
    else:
        layout = create_layout()
    window = sg.Window('Mastery Manager', layout, resizable=True, finalize=True)
    return window


def update_icon(window):
    global Icon_size
    # Update summoner icon
    summoner_data = load_data_from_json('summoner_data')
    if summoner_data['profileIconId'] == 0:
        summoner_icon = Image.open('MasteryManager/images/icon0.jpg')
    else:
        summoner_icon = Image.open(f'MasteryManager/temp/icons/icon{summoner_data["profileIconId"]}.jpg')
    summoner_icon = summoner_icon.resize(Icon_size)
    summoner_icon = ImageTk.PhotoImage(summoner_icon)
    window['-ICON-'].update(data=summoner_icon)


def update_champion_squares(window, mastery_data=None):
    global champion_square_size
    # Update champion squares
    if not mastery_data:
        mastery_data = load_data_from_json('mastery_data')

    for champ in mastery_data:
        if champ["championId"] == 0:
            continue

        #assemble_image(champ["championId"], champ["championLevel"])
        #champion_square = Image.open(f'MasteryManager/temp/champions/assembled_champ{champ["championId"]}.jpg')

        champion_square = Image.open(f'MasteryManager/temp/champions/champ{champ["championId"]}.jpg')
        champion_square = champion_square.resize(champion_square_size)
        champion_square = ImageTk.PhotoImage(champion_square)
        window[f'-CHAMPION-{champ["championId"]}-IMAGE-'].update(data=champion_square)


def load_window_location():
    # Load window location from file
    if os.path.exists('MasteryManager/temp/window_location.json'):
        with open('MasteryManager/temp/window_location.json') as file:
            window_location = json.load(file)
        return window_location
    
def save_window_location(location):
    # Save window location to file
    window_location = location
    if not os.path.exists('MasteryManager/temp'):
        os.makedirs('MasteryManager/temp')
    with open('MasteryManager/temp/window_location.json', 'w') as file:
        json.dump(window_location, file)


def loading_screen(window=None, start=None, stop=None, window_location=None):
    if start:
        # Create loading screen
        layout = [
            [sg.Text('Loading...', font=('Helvetica', 60))]
        ]
        loading_window = sg.Window('Mastery Manager - Loading', layout, finalize=True)

        loading_window.move(window_location[0], window_location[1])

        event, values = loading_window.read(timeout=0)

        return loading_window
    
    if stop:
        # Close loading screen
        window.close()

# Run the app
def run_app():
    # Create window with layout from the create_layout() function
    window = update_window()

    # Load window location from file and move window if possible
    window_location = load_window_location()
    if window_location:
        window.move(window_location[0], window_location[1])

    # Load summoner icon in Header
    update_icon(window)

    # Load champion squares in Body
    update_champion_squares(window)

    # Event loop
    while True:
        # Read events and values from window
        event, values = window.read()

        # End loop if window is closed
        if event == sg.WINDOW_CLOSED:
            break

        # Update window if input is given or update button is pressed
        elif (event == '-SUBMIT-' and values['-INPUT-'] != '') or event == '-UPDATE-':
            # store window location and save to file
            window_location = window.CurrentLocation()
            save_window_location(window_location)

            # Create loading screen
            loading_window = loading_screen(start=True, window_location=window_location)

            # Get all assets based on input
            if event == '-SUBMIT-':
                get_all_assets(values['-INPUT-'])
            elif event == '-UPDATE-':
                summoner_data = load_data_from_json('summoner_data')
                get_all_assets(summoner_data['name'])
            
            # Close loading screen
            loading_screen(loading_window, stop=True)
            
            # Save scroll position in mastery column
            scroll_position = window['-MASTERY-'].Widget.canvas.yview()[0]

            # close and update window, moving it to the same location as before
            window.close()
            window = update_window()
            window.move(window_location[0], window_location[1])

            # Load summoner icon in Header and champion squares in Body
            update_icon(window)
            update_champion_squares(window)

            # Scroll to the same position as before if Update was pressed
            if event == '-UPDATE-':
                window['-MASTERY-'].Widget.canvas.yview_moveto(scroll_position)
        
        # Applie filter or sort mastery data
        elif event == '-FILTER-' or event == '-SORT-':
            # load mastery data from file
            mastery_data = load_data_from_json('mastery_data')

            # apply filter or sort
            if values['-FILTER-'] == 'Remove lv 7':
                mastery_data = [champ for champ in mastery_data if champ['championLevel'] != 7]

            elif values['-FILTER-'] == 'Remove lv >5':
                mastery_data = [champ for champ in mastery_data if champ['championLevel'] <= 5]

            elif values['-FILTER-'] == 'Remove lv >4':
                mastery_data = [champ for champ in mastery_data if champ['championLevel'] <= 4]
            
            elif values['-SORT-'] == 'By level, highest first':
                mastery_data = sorted(mastery_data, key=lambda k: k['championLevel'], reverse=True)

            elif values['-SORT-'] == 'By level, lowest first':
                mastery_data = sorted(mastery_data, key=lambda k: k['championLevel'])
            
            elif values['-SORT-'] == 'By points, highest first':
                mastery_data = sorted(mastery_data, key=lambda k: k['championPoints'], reverse=True)

            elif values['-SORT-'] == 'By points, lowest first':
                mastery_data = sorted(mastery_data, key=lambda k: k['championPoints'])
            
            # close and update window, moving it to the same location as before
            window.close()
            window = update_window(mastery_data)
            window.move(window_location[0], window_location[1])

            # Load summoner icon in Header and champion squares in Body
            update_icon(window)
            update_champion_squares(window, mastery_data)

        # Clear filters and sort restoring the window to its original state
        elif event == '-CLEAR-':
            print('Filters cleared')
            # close and update window, moving it to the same location as before
            window.close()
            window = update_window()
            window.move(window_location[0], window_location[1])
            
            # Load summoner icon in Header and champion squares in Body
            update_icon(window)
            update_champion_squares(window)         

        # Filter champion names based on input
        elif event == '-FILTER-INPUT-':
            mastery_data = load_data_from_json('mastery_data')
            for champ in mastery_data:

                if values['-FILTER-INPUT-'].lower() not in champ['championName'].lower():
                    #window[f"-CHAMPION-{champ['championId']}-IMAGE-"].update(visible=False)
                    window[f"-CHAMPION-{champ['championId']}-IMAGE-"].hide_row()
                    #window[f"-CHAMPION-{champ['championId']}-NAME-"].update(visible=False)
                    window[f"-CHAMPION-{champ['championId']}-NAME-"].hide_row()            
                    #window[f"-CHAMPION-{champ['championId']}-LEVEL-"].update(visible=False)
                    window[f"-CHAMPION-{champ['championId']}-LEVEL-"].hide_row()
                    #window[f"-CHAMPION-{champ['championId']}-POINTS-"].update(visible=False)
                    window[f"-CHAMPION-{champ['championId']}-POINTS-"].hide_row()

                else:
                    #window[f"-CHAMPION-{champ['championId']}-IMAGE-"].update(visible=True)
                    window[f"-CHAMPION-{champ['championId']}-IMAGE-"].unhide_row()
                    #window[f"-CHAMPION-{champ['championId']}-NAME-"].update(visible=True)
                    window[f"-CHAMPION-{champ['championId']}-NAME-"].unhide_row()                
                    #window[f"-CHAMPION-{champ['championId']}-LEVEL-"].update(visible=True)
                    window[f"-CHAMPION-{champ['championId']}-LEVEL-"].unhide_row()
                    #window[f"-CHAMPION-{champ['championId']}-POINTS-"].update(visible=True)
                    window[f"-CHAMPION-{champ['championId']}-POINTS-"].unhide_row()
    
    # Close window and end application
    window.close()
    

if __name__ == "__main__":
    run_app()
