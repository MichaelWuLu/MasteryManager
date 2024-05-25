import requests
import os


def get_summoner_icon(profileIconId):
    request = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/{profileIconId}.jpg"
    response = requests.get(request)

    if not os.path.exists(f"temp/icons"):
        os.makedirs(f"temp/icons")

    with open(f"temp/icons/icon{profileIconId}.jpg", "wb") as f:
        f.write(response.content)


def get_champion_square(championId):
    request = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-icons/{championId}.png"
    response = requests.get(request)

    if not os.path.exists(f"temp/champions"):
        os.makedirs(f"temp/champions")

    with open(f"temp/champions/champ{championId}.png", "wb") as f:
        f.write(response.content)
