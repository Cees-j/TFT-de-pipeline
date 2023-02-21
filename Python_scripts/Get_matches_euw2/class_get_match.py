from Classes import GetInformation, API_caller, csv_store_function
from api_key import API_KEY
'''This will return someones match history and store it in a csv'''
Get_puuid = GetInformation('puuid', 'csv-store-10001', 'Get_PUUID_euw.csv', 2)

# print(Get_puuid.download_csv_file())

returned_csv_object_containing_puuid = Get_puuid.download_csv_file() # This downloads a file
# from GCS and then makes a list which api calls can be made from

# print(returned_csv_object_containing_puuid)

get_matches_api_caller = API_caller(returned_csv_object_containing_puuid,
'europe', 
api_endpoint='tft/match/v1/matches/by-puuid/{specific}/ids?api_key={API_KEY}', API_KEY=
API_KEY, entrypoint_in_return_json=None)

# print(get_matches_api_caller.make_api_call())

dataframe_from_api = get_matches_api_caller.make_api_call()

csv_store_function(dataframe_from_api, 'euw-matches.csv')

# May have made this more confusing by making it a class, dont know if theres so much distinction
# between the methods that this wasnt a good idea. 
# I have to make it into a list, then into a dataframe in the store section
# then upload that dataframe as csv.. EH ITS OK
# No it doesnt work, I need to query it, get back that row, and insert that data into
# whats already there. List doesnt work.
# So basically the question is how can i append to a dataframe += 
# Should just be one column of data matches for 1 guy, next column inserted another chunk,
# Damn maybe made it too complicated using classes
# So you instantiate the empty dataframe, then need to join the returning data for 
# each call. So its fine if theres only 1 call for chall data, but everything else
# needs to append 