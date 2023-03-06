from Classes_2 import GetInformation, api_string_constructor, process_response_object, csv_store_function
import os
# from api_key import API_KEY
'''This needs to get some information from the get_chall csv which is in storage, 
then it needs to create and request a query string for each of those names
then it needs aggregate a dataframe and put it into storage.'''

API_KEY = os.environ.get('API_KEY')

def entrypoint(req):
    print(req)
    Get_info = GetInformation('name', 'csv-store-10001', 'euw_chall.csv', 1)
    initial_data = Get_info.download_csv_file()
    print('Data to iterate over:', initial_data)
    response_data = api_string_constructor(initial_data, 
                       api_endpoint="https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{specific}?api_key={API_KEY}",
                       API_KEY=API_KEY)
    print(response_data)

    processed_data = process_response_object(response_data, nested_key=None)
    csv_store_function(processed_data, 'sailmate')
    return('200, ok')

