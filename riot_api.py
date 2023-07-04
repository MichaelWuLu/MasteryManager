import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()  # loads variables from .env.


def get_by_summoner_name(summonerName):
    api_key = os.getenv('API_KEY')
    api_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key="
    request = api_url + str(api_key)
    response = requests.get(request)
    print(response)

    with open('temp/summonerName.json', 'w') as json_file:
        json.dump(response.json(), json_file, indent=4)


def get_value_from_json(file, key):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
        output = data[key]
        return output


def get_mastery_score_by_calculation():
    with open('temp/mastery.json', 'r') as json_file:
        data = json.load(json_file)
        cumulative = 0
        for dict in data:
            lvl = dict['championLevel']
            cumulative = cumulative + lvl
        return cumulative


def get_mastery_by_summoner_id():
    encryptedSummonerId = get_value_from_json('temp/summonerName.json', 'id')

    api_key = os.getenv('API_KEY')
    api_url = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{encryptedSummonerId}?api_key="
    request = api_url + str(api_key)
    response = requests.get(request)
    print(response)

    with open('temp/mastery.json', 'w') as json_file:
        json.dump(response.json(), json_file, indent=4)


def list_of_champions_with_mastery():
    with open('temp/mastery.json','r') as json_file:
        data = json.load(json_file)
        for champ in data:
            champion = (champ["championId"], champ["championLevel"], champ["championPoints"], champ["chestGranted"], champ["tokensEarned"])
            print(str(champion) + '\n')

#get_by_summoner_name('Murzak')
#get_mastery_by_summoner_id()
#list_of_champions_with_mastery()