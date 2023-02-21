from Classes_2 import GetInformation, api_string_constructor, process_response_object, csv_store_function
from api_key import API_KEY
'''This will return someones match history and store it in a csv'''
# f"https://{platform}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"

# get chall -> get puuid (takes names from chall data set) -> get match (takes puuid from puuid)

Get_info = GetInformation('puuid', 'csv-store-10001', 'sailmate', 2)

initial_data = Get_info.download_csv_file()

print('Data to iterate over:', initial_data)

response_data = api_string_constructor(initial_data,
                        api_endpoint="https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{specific}/ids?api_key={API_KEY}",
                        API_KEY=API_KEY)

print(response_data)

processed_data = process_response_object(response_data, nested_key=None)

print (processed_data)

csv_store_function(processed_data, 'sailmate2')