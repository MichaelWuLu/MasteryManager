import requests


def get_summoner_icon(profileIconId):
    request = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/profile-icons/{profileIconId}.jpg"
    result = requests.get(request)
    print(result)

    with open(f"temp/icon{profileIconId}.jpg", "wb") as f:
        f.write(result.content)


def get_champion_square(championId):
    request = f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-tiles/{championId}/{championId}000.jpg"
    response = requests.get(request)
    print(response)

    with open(f"temp/champ{championId}.jpg", "wb") as f:
        f.write(response.content)
