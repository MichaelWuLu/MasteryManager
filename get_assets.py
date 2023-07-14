import requests


def get_summoner_icon(profileIconId):
    request = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/{profileIconId}.jpg"
    response = requests.get(request)
    print(f"Get icon: {response}")

    with open(f"temp/icons/icon{profileIconId}.jpg", "wb") as f:
        f.write(response.content)


def get_champion_square(championId):
    request = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-tiles/{championId}/{championId}000.jpg"
    response = requests.get(request)
    print(f"Get champ {championId}: {response}")

    with open(f"temp/champions/champ{championId}.jpg", "wb") as f:
        f.write(response.content)
