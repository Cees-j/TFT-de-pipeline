import pandas as pd
import requests

# Set up your API key
api_key = "RGAPI-5e0264ae-9c42-4465-bcfa-332268218369 "
platform = "europe"
puuid = "vNT_SxEHkPpZd0zJW0VvnK7u3rDyfn3cfofpce6c_tzsS6hzcH-t7mQM6W0yLO-1Y4RbMxKQFqQFQw"

def get_match_by_puuid(platform, puuid):
    # Different platform letters than other links
    # Get a list of match IDs for the specified player
    match_ids_by_puuid_url = f"https://{platform}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Riot-Token": "RGAPI-5e0264ae-9c42-4465-bcfa-332268218369"
    }
    # This retrieves a list of the match ids for the puuid specified
    matches_for_puuid_response = requests.get(match_ids_by_puuid_url, headers=header)
    match_ids = matches_for_puuid_response.json()
    print(len(match_ids))

    # Get detailed match information for each match, I only want info not metadata
    matches = []
    for match_id in match_ids:
        match_url = f"https://{platform}.api.riotgames.com/tft/match/v1/matches/{match_id}"
        individual_match_response = requests.get(match_url, headers=header)
        match = individual_match_response.json()
        print(match.keys())
        print(match['metadata'])
        print(match['info'])
        
        matches.append(match['info'])
 
    df = pd.DataFrame(matches)
  
    df.to_csv("matches3.csv", index=False)

get_match_by_puuid(puuid=puuid, platform=platform)