from Classes_2 import GetInformation, api_string_constructor, process_response_object, csv_store_function
# from api_key import API_KEY
import os
'''Read the match history dataframe, for each entry, 
make a request'''
API_KEY = os.environ.get('API_KEY')

def entrypoint(req):
    print(req)
    for i in range(100000):
        try:
            Get_info = GetInformation('0', 'csv-store-10001', 'sailmate2', i)
            initial_data = Get_info.download_csv_file()


            print('Data to iterate over:', initial_data)
        except IndexError as ie:
            print('End of file reached')
            break


        response_data = api_string_constructor(initial_data,
        api_endpoint="https://europe.api.riotgames.com/tft/match/v1/matches/{specific}?api_key={API_KEY}",
        API_KEY=API_KEY)

        print (response_data)

        processed_data = process_response_object(response_data, nested_key=None)

        print(processed_data)

        csv_store_function(processed_data, 'sailmate3')