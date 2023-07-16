import requests
import os


def get_summoner_icon(profileIconId):
    request = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/{profileIconId}.jpg"
    response = requests.get(request)

    if not os.path.exists(f"MasteryManager/temp/icons"):
        os.makedirs(f"MasteryManager/temp/icons")

    with open(f"MasteryManager/temp/icons/icon{profileIconId}.jpg", "wb") as f:
        f.write(response.content)


def get_champion_square(championId):
    request = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-tiles/{championId}/{championId}000.jpg"
    response = requests.get(request)

    if not os.path.exists(f"MasteryManager/temp/champions"):
        os.makedirs(f"MasteryManager/temp/champions")

    with open(f"MasteryManager/temp/champions/champ{championId}.jpg", "wb") as f:
        f.write(response.content)
