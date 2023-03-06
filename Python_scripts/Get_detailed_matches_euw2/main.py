from Classes_2 import GetInformation, api_string_constructor, process_response_object, csv_store_function
import os
import time

API_KEY = os.environ.get('API_KEY')

def entrypoint(req, api_calls=0):  
    '''We set api_calls to 0 to ensure we can manage rate limits. We take info
    from csv file of match history of challengers, then we iterate over the first
    column of that, which in this case is going to be each players first game of 20,
    Then with that match you're using its match id to make an api call and append it to a list
    that list is then being iterated to make into an api call and return detailed match data
    and store it in a unqiue csv file. 
    Will have multiple csv files which can be imported into BigQuery as large data dump, from
    which other tables can be made'''
    
    print(req)
    count = 0
    for i in range(20):
        if api_calls % 25 == 0:
            time.sleep(30)
        print('API CALLS =', api_calls)
        try:
            Get_info = GetInformation('0', 'csv-store-10001', 'sailmate2', i)
            initial_data = Get_info.download_csv_file()


            print('Data to iterate over:', initial_data)
            api_calls += len(initial_data)
        except IndexError as ie:
            print('End of file reached')
            break


        response_data = api_string_constructor(initial_data,
        api_endpoint="https://europe.api.riotgames.com/tft/match/v1/matches/{specific}?api_key={API_KEY}",
        API_KEY=API_KEY)

        print (response_data)

        processed_data = process_response_object(response_data, nested_key=None)

        print (processed_data)

        csv_store_function(processed_data, 'sailmate3')
        print (f'iteration {count} completed')
        count +=1
    
    return ('200')
