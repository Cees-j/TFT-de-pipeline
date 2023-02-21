from Classes import API_caller, csv_store_function
from api_key import API_KEY
'''The api caller in this case is 1, there are not multiple entries instead a list is given back
region for this is euw1
api_version refers to endpoint'''

get_chall_api_caller = API_caller(['1'], region='euw1',
api_endpoint='tft/league/v1/challenger?api_key={API_KEY}',
API_KEY=API_KEY, entrypoint_in_return_json='entries')

# get_chall_data = get_chall_api_caller.make_api_call

# Calling store with file name of Get_Chall2_euw.csv on the returning api dataframe
# from making the api call
csv_store_function(get_chall_api_caller.make_api_call(), 'Get_Chall2_euw.csv')


