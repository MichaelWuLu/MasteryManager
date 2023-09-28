# Description: This file contains functions that download assets from community dragon and save them locally.

import requests
import os
import json
from riot_api import get_by_summoner_name, get_mastery_by_summoner_id, get_value_from_json


def get_summoner_icon(profileIconId):
    if not os.path.exists(f"temp/icons"):
        os.makedirs(f"temp/icons")

    if os.path.exists(f"temp/icons/icon{profileIconId}.jpg"):
        return
    
    request = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/{profileIconId}.jpg"
    response = requests.get(request)

    with open(f"temp/icons/icon{profileIconId}.jpg", "wb") as f:
        f.write(response.content)


def get_champion_square(championId):
    if not os.path.exists(f"temp/champions"):
        os.makedirs(f"temp/champions")
    
    if os.path.exists(f"temp/champions/champ{championId}.jpg"):
        return
    
    request = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-tiles/{championId}/{championId}000.jpg"
    response = requests.get(request)

    with open(f"temp/champions/champ{championId}.jpg", "wb") as f:
        f.write(response.content)


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

