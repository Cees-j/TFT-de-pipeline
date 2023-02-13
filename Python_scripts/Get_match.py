import pandas as pd
import requests
from envrio_variables import API_KEY
import time 
# Set up your API key
header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Riot-Token": API_KEY
    }
platform = "europe"
puuid = "q7Czl1-xj3ykT0mRGWrauBfkUAJi2Gh4e1kA6WbUmlmEpcSlWOhl-e_nSlVjIsmBfcjPdAgfacXefQ"

puuid_names_df = pd.read_csv("puuid_names_data_euw1.csv") ## reading the local df so i can iterate over puuids and insert into get match

def get_match_by_puuid(platform, puuid, header):
    '''Per puuid, this function makes a call to get the match ids, which returns 20 match ids, which is the players recent history
    Then once you have the match ids, you need to do something else with them.'''
    print('Getting matches by puuid')
    match_ids_by_puuid_url = f"https://{platform}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"
    header = header
    # This retrieves a list of the match ids for the puuid specified
    matches_for_puuid_response = requests.get(match_ids_by_puuid_url, headers=header)
    match_ids = matches_for_puuid_response.json()

    print (match_ids)
    return match_ids

def get_detailed_match_information(match_ids, header):
    '''Gets detailed match information, gets info, and then more detailed one, the more 
    detailed one contains the actual matches and all players, has lots of nested data returned
    matches.csv returns the match history.
    detailed_matches.csv returns the configuration of all the players within those matches'''
    time.sleep(1.5)
    print('getting detailed match information')

    matches = []
    detailed_match_info = []
    for match_id in match_ids:
        match_url = f"https://{platform}.api.riotgames.com/tft/match/v1/matches/{match_id}"
        individual_match_response = requests.get(match_url, headers=header)
        print(individual_match_response)
        match = individual_match_response.text
        print(match)

        
        matches.append(match)
        # detailed_match_info.append(match['info']['participants'])
 
    df = pd.DataFrame(matches)
    df.to_json("matches_json_String.json")
    

    # detailed_match_info_df = pd.DataFrame(detailed_match_info, columns=['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8'])
    # detailed_match_info_df.to_csv("detailed_matches3.csv", index=False)


get_detailed_match_information(get_match_by_puuid(puuid=puuid, platform=platform, header=header), header)

