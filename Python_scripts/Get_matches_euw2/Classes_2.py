import csv
import requests
from google.cloud import storage
import pandas as pd
from api_key import API_KEY
import os
import logging
import csv
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json' 

class StorageError(Exception):
    '''Custom exception for storage-related errors'''
    pass

class GetInformation:
    def __init__(self, column: str, dl_bucket: str, dl_filename: str,  extract_col: int):
        '''
        CONSULT STORAGE BUCKETS TO DECIDE WHAT PARAMETERS YOU WANT
        This class can take an item from a csv store, then iterate over that file
        and take whichever column it is you need from the csv, and store that in a list, which 
        can then be given to another class to make api calls.
        Would have to examine the csv data in browser or by other means to determine the column
        and extract_col'''

        self.column = column
        self.download_bucket = dl_bucket
        self.download_filename = dl_filename
        self.extract_col = extract_col
        self.result_list = []


    def process_csv_file(self, csv_reader): 
        print('Now processing file and extracting what needs to be')
        extract_col = self.extract_col  
        self.reader = csv_reader 
        
        next(self.reader) # Skips column titles

        count = 0
        for row in csv_reader:
            count += 1
            if count > 25:
                break
            if len(row)>2:
                extracted_row = row[extract_col]
                #print(extracted_row)
                self.result_list.append(extracted_row)
                # result = api_call(puuid)
        return self.result_list

    def download_csv_file(self):
        file_name = self.download_filename
        print(f'Downloading file {file_name} from csv-store')
        
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.download_bucket)
        blob = bucket.blob(file_name)
        contents = blob.download_as_string().decode('utf-8')

        csv_reader = csv.reader(contents.split('\n'))
        self.process_csv_file(csv_reader)

        print('Finished processing, returned iterable')
        return self.result_list
    


def process_response_object(res_json, nested_key):
    '''If there is nested data from the response object then this function
    will dig down and get the level of data you need, otherwise it will just make 
    it into a dataframe which can be then be used to turn into a csv and stored'''
    print('Processing response object')
    if nested_key:
        dataframe = pd.DataFrame(res_json[0][nested_key])
    else: 
        dataframe = pd.DataFrame(res_json)
    return (dataframe)

def api_string_constructor(search_items: list, api_endpoint: str, API_KEY):
    """This is going to take a list of things that need to be iterated over and create
    a query string. Will return a request response object
    If using get chall pass it ['1'] otherwise pass it the return from Get_information"""
    print('Constructing and requesting api')
    response_data_list = []
    count = 0 
    for item in search_items: 
        count += 1 
        if count > 5:
            break
        try:
            url = api_endpoint.format(specific=item, API_KEY=API_KEY)
            response = requests.get(url)
        
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
        
        if response.status_code == 200:
            response_data = response.json()
            response_data_list.append(response_data)
        else:
            logging.error(response.status_code)
            
    return response_data_list
        



def csv_store_function(data, file_name):
    '''Takes a dataframe, turns it into a csv, and then stores in under a given filename'''
    print(data)
    bucket_name = 'csv-store-10001' 
 

    csv_data = data.to_csv(index=False)
    try:
        print('Attemping to store csv')
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(csv_data)
        logging.info(f'{file_name} stored in {bucket_name}')
        return (f'200, {file_name} storage Complete')
    except Exception as e:
        raise StorageError(f"Failed to store CSV data: {str(e)}")
    
    

if __name__ == "__main__":
    info = GetInformation('puuid', 'csv-store-10001', 'Get_PUUID_euw.csv', 2)

    info.download_csv_file()
    info_list = info.result_list
    get_matches_api_caller = API_caller(info_list, 'europe', 'tft/match/v1/matches/by-puuid/{specific}/ids?api_key={API_KEY}', API_KEY=
                                        API_KEY)
    get_matches_api_caller.make_api_call()

# f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={API_KEY}"
# f'https://{region}.api.riotgames.com/tft/league/v1/challenger'
# f"https://{platform}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"

