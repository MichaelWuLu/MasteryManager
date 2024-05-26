# Description: This file contains functions that download assets from community dragon and save them locally.

import requests
import os
import json
from riot_api import get_summoner_by_riot_id, get_mastery_by_puuid, get_value_from_json


def get_profile_icon(profileIconId):
    if not os.path.exists(f"temp/icons"):
        os.makedirs(f"temp/icons")

    if os.path.exists(f"temp/icons/icon{profileIconId}.jpg"):
        return
    
    request = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/{profileIconId}.jpg"
    response = requests.get(request)

    with open(f"temp/icons/icon{profileIconId}.jpg", "wb") as f:
        f.write(response.content)


def get_champion_square(championId):
    request = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{championId}.png"
    response = requests.get(request)

    if not os.path.exists(f"temp/champions"):
        os.makedirs(f"temp/champions")

    with open(f"temp/champions/champ{championId}.png", "wb") as f:
        f.write(response.content)


def get_all_assets(riotId):
    # Get riotId.json containing the correct summoners information
    if not os.path.exists('temp/riotId.json'):
        get_summoner_by_riot_id(riotId)
    else:
        with open('temp/riotId.json') as file:
            riotId_data = json.load(file)
        if riotId != f"{riotId_data['gameName']}#{riotId_data['tagLine']}":
            get_summoner_by_riot_id(riotId)

    # Get summoner icon if it doesn't exist
    profileIconId = get_value_from_json('temp/summoner.json', 'profileIconId')
    if not os.path.exists(f'temp/icons/icon{profileIconId}.jpg'):
        get_profile_icon(profileIconId)
    
    # Get/Update mastery.json containing the summoners mastery information
    get_mastery_by_puuid()
    # Get champion squares if they don't exist
    with open('temp/mastery.json') as file:
        mastery_data = json.load(file)

    for champ in mastery_data:
        if not os.path.exists(f"temp/champions/champ{champ['championId']}.jpg"):
            get_champion_square(champ['championId'])

