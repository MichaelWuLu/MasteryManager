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


def load_data_from_json(wanted_data):
    if wanted_data == ('summoner_data') and os.path.exists('temp/summonerName.json'):
        # Load summonerName.json and mastery.json
        with open('temp/summonerName.json') as file:
            summoner_data = json.load(file)
        return summoner_data
    elif wanted_data == ('summoner_data'):
        summoner_data = {
            'name': 'SummonerName', 
            'profileIconId': 0
            }
        return summoner_data

    if wanted_data == ('mastery_data') and os.path.exists('temp/mastery.json'):
        with open('temp/mastery.json') as file:
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



