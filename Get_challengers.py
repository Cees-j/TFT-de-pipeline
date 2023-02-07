import pandas as pd
import requests
from envrio_variables import API_KEY


headers = {"X-Riot-Token": API_KEY}

# Gets challenger ladder data by region and formats into csv
def get_chall_ladder_data(region):
    chall_response = requests.get(f'https://{region}.api.riotgames.com/tft/league/v1/challenger', headers=headers)
    chall_data = chall_response.json()

    challenger_df = pd.DataFrame(chall_data['entries'])
    challenger_df.drop(columns=['veteran', 'freshBlood'], axis=1, inplace=True)
    challenger_df.to_csv(f"challenger_data_3_{region}.csv", index=False)



get_chall_ladder_data('euw1')