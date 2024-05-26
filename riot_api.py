# Description: This file contains all the functions used to get data from the Riot API and the community dragon.

import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()  # loads variables from .env.


# Get puuid by riotId (gameName#tagline) saving the response in a json file called riotId.json
def get_puuid_by_riot_id(riotId, accountRegion='europe'):
    gameName = riotId.split('#')[0]
    tagLine = riotId.split('#')[1]

    api_key = os.getenv('API_KEY')
    api_url = f"https://{accountRegion}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key="
    request = api_url + str(api_key)
    response = requests.get(request)
    print(f"Get puuid: {response}")

    # If riotId doesn't exist, return 404
    if response.status_code == 404:
        return 404

    if not os.path.exists('temp/'):
        os.makedirs('temp/')

    with open('temp/riotId.json', 'w') as file:
        json.dump(response.json(), file, indent=4)


def get_summoner_by_riot_id(riotId, leagueRegion='euw1'):
    if not os.path.exists('temp/riotId.json'):
        get_puuid_by_riot_id(riotId)
    elif not get_value_from_json('temp/riotId.json', 'gameName') == riotId.split('#')[0]:
        get_puuid_by_riot_id(riotId)
    
    puuid = get_value_from_json('temp/riotId.json', 'puuid')

    api_key = os.getenv('API_KEY')
    api_url = f"https://{leagueRegion}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key="
    request = api_url + str(api_key)
    response = requests.get(request)
    print(f"Get summoner: {response}")

    # If summoner doesn't exist, return 404
    if response.status_code == 404:
        return 404

    if not os.path.exists('temp/'):
        os.makedirs('temp/')

    with open('temp/summoner.json', 'w') as file:
        json.dump(response.json(), file, indent=4)


def get_value_from_json(file, key):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        output = data[key]
        return output


def get_mastery_by_puuid():
    # Get latest league version
    league_version = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]

    puuid = get_value_from_json('temp/riotId.json', 'puuid')

    api_key = os.getenv('API_KEY')
    api_url = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}?api_key="
    request = api_url + str(api_key)
    response = requests.get(request)
    print(f"Get Mastery: {response}")

    if not os.path.exists('temp/'):
        os.makedirs('temp/')

    get_champion_names()
    with open(f'temp/champions/champion{league_version}.json', 'r') as file:
        champion_names = json.load(file)

    with open('temp/mastery.json', 'w') as file:
        champions = response.json()
        for champ in champion_names:
            for mastery in champions:
                if champ['championId'] == mastery['championId']:
                    mastery['championName'] = champ['championName']

        json.dump(champions, file, indent=4)


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
    if wanted_data == ('riotId_data') and os.path.exists('temp/riotId.json'):
        # Load riotId.json
        with open('temp/riotIdsummonerName.json') as file:
            riotId_data = json.load(file)
        return riotId_data
    elif wanted_data == ('riotId_data'):
        # return placeholder data if no riotId data is found
        riotId_data = {
            'gameName': 'Account name',
            }
        return riotId_data

    if wanted_data == ('summoner_data') and os.path.exists('temp/summonerName.json'):
        # Load summonerName.json
        with open('temp/summonerName.json') as file:
            summoner_data = json.load(file)
        return summoner_data
    elif wanted_data == ('summoner_data'):
        # return placeholder data if no summoner data is found
        summoner_data = {
            'profileIconId': 0
            }
        return summoner_data

    if wanted_data == ('mastery_data') and os.path.exists('temp/mastery.json'):
        # Load mastery.json
        with open('temp/mastery.json') as file:
            mastery_data = json.load(file)

            mastery_data = sorted(mastery_data, key=lambda k: (k['championLevel'], k['championPoints']), 
                                  reverse=True)
        return mastery_data
    
    elif wanted_data == ('mastery_data'):
        # return placeholder data if no mastery data is found
        mastery_data = [
            {'championId': 0, 
             'championName': 'No mastery data found',
             'championLevel': 0,
             'championPoints': 0
            }
        ]
        return mastery_data
