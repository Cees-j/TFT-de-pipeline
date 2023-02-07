import pandas as pd 
import requests
from envrio_variables import API_KEY

# Should return PUUID of a summoner 
chall_df = pd.read_csv("challenger_data_3_euw1.csv") ## reading locally so can iterate

def format_dataframe_and_isolate_names(dataframe):
    sorted_chall_df = dataframe.sort_values(by=['leaguePoints'], ascending=False).head(3)
    chall_names = sorted_chall_df['summonerName'].tolist()
    return chall_names

chall_names = format_dataframe_and_isolate_names(chall_df)

def get_puuid(names, platform):
    '''Need this act on the file that was gained through get_challenger, and iterate over all the names
    making sure the platform is correct. Then this will provide all the PUUIDs, and then put that into a 
    DF containing, name, platform, puuid
    
    Due to api limits doing only the top 80 per region'''
    api_return_data = []


    for name in names:
        try:
            url = f"https://{platform}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{name}?api_key={API_KEY}"
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")


        if response.status_code == 200:
            summoner_data = response.json()
            puuid = summoner_data['puuid']
            print(f"PUUID of summoner '{name}' on platform '{platform}' is: {puuid}")
            api_return_data.append({'name': name, 'region': platform, 'puuid': puuid})
        else:
            print(f"Error retrieving summoner data: {response.status_code}")

    puuid_dataframe = pd.DataFrame(api_return_data, columns=['name', 'region', 'puuid'])
    print(puuid_dataframe)

    puuid_dataframe.to_csv(f"puuid_names_data_{platform}.csv", index=False)
    return puuid_dataframe

get_puuid(chall_names, platform='euw1')