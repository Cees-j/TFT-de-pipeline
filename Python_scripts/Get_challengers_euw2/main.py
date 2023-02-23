from Classes_2 import process_response_object, csv_store_function, api_string_constructor
import os 

API_KEY = os.environ.get('API_KEY')

'''This is saying, for one iteration, make a request to this url, and then
process that data to achieve your level of nested data that you want, and then
store that in the csv-store with a certain file name'''

def entrypoint(req):
    print(req)
    response_data = api_string_constructor(['1'], 
                       api_endpoint='https://euw1.api.riotgames.com/tft/league/v1/challenger?api_key={API_KEY}',
                       API_KEY=API_KEY)

    processed_data = process_response_object(response_data, nested_key='entries')

    csv_store_function(processed_data, 'euw_chall.csv')

    return('200, ok')



# response_data = api_string_constructor(['1'], 
#                        api_endpoint='https://euw1.api.riotgames.com/tft/league/v1/challenger?api_key={API_KEY}',
#                        API_KEY=API_KEY)

# processed_data = process_response_object(response_data, nested_key='entries')

# csv_store_function(processed_data, 'euw_chall.csv')