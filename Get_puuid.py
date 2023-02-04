import requests


# Should return PUUID of a summoner 
api_key = "RGAPI-5e0264ae-9c42-4465-bcfa-332268218369 "
summoner_name = "TFTMarx"
platform = "euw1"

def get_puuid(summoner_name, platform):

    url = f"https://{platform}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        summoner_data = response.json()
        puuid = summoner_data['puuid']
        print(f"PUUID of summoner '{summoner_name}' on platform '{platform}' is: {puuid}")
    else:
        print(f"Error retrieving summoner data: {response.status_code}")

get_puuid(summoner_name=summoner_name, platform=platform)