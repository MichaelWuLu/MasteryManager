# Description: This file contains all the functions that are used to get data from the Riot API.

import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()  # loads variables from .env.


# Get summoner by summonerName saving the response in a json file called summonerName.json
def get_by_summoner_name(summonerName):
    api_key = os.getenv('API_KEY')
    api_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key="
    request = api_url + str(api_key)
    response = requests.get(request)
    print(f"Get summoner: {response}")

    # If summonerName doesn't exist, return 404
    if response.status_code == 404:
        return 404

    if not os.path.exists('temp/'):
        os.makedirs('temp/')

    with open('temp/summonerName.json', 'w') as json_file:
        json.dump(response.json(), json_file, indent=4)


def get_value_from_json(file, key):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        output = data[key]
        return output


def get_mastery_by_summoner_id():
    # Get latest league version
    league_version = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]

    encryptedSummonerId = get_value_from_json('temp/summonerName.json', 'id')

    api_key = os.getenv('API_KEY')
    api_url = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{encryptedSummonerId}?api_key="
    request = api_url + str(api_key)
    response = requests.get(request)
    print(f"Get Mastery: {response}")

    if not os.path.exists('temp/'):
        os.makedirs('temp/')

    get_champion_names()
    with open(f'temp/champions/champion{league_version}.json', 'r') as json_file:
        champion_names = json.load(json_file)

    with open('temp/mastery.json', 'w') as json_file:
        champions = response.json()
        for champ in champion_names:
            for mastery in champions:
                if champ['championId'] == str(mastery['championId']):
                    mastery['championName'] = champ['championName']

        json.dump(champions, json_file, indent=4)


def get_champion_names():
    # Get latest league version
    league_version = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]

    if not os.path.exists('temp/champions/'):
        os.makedirs('temp/champions/')
        
    # Get champion.json
    if not os.path.exists(f'temp/champions/champion{league_version}.json'):
        get_champion_json(league_version)
    else:
        for file in os.listdir('temp'):
            if file.endswith(f'champion{league_version}.json'):
                get_champion_json(league_version)


def get_champion_json(league_version):
    request = f"http://ddragon.leagueoflegends.com/cdn/{league_version}/data/en_US/champion.json"
    response = requests.get(request)
    print(f"Get champion.json: {response}")

    with open(f'temp/champions/champion{league_version}.json', 'w') as json_file:
        data = response.json()
        exstacted_data = []
        for item in data['data']:
            exstracted_item = {
                'championId': data['data'][item]['key'],
                'championName': data['data'][item]['name'],
            }
            exstacted_data.append(exstracted_item)

        json.dump(exstacted_data, json_file, indent=4)


def load_data_from_json(wanted_data):
    if wanted_data == ('summoner_data') and os.path.exists('temp/summonerName.json'):
        # Load summonerName.json and mastery.json
        with open('temp/summonerName.json') as file:
            summoner_data = json.load(file)
        return summoner_data
    elif wanted_data == ('summoner_data'):
        # return empty list if no summoner data is found
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
        # return empty list if no mastery data is found
        mastery_data = [
            {'championId': 0, 
             'championName': 'No mastery data found',
             'championLevel': 0,
             'championPoints': 0
            }
        ]
        return mastery_data
