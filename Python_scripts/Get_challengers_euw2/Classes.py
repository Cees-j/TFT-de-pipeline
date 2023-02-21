import csv
import requests
from google.cloud import storage
import pandas as pd
from api_key import API_KEY
import os
import logging
import csv
# f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={API_KEY}"
# f'https://{region}.api.riotgames.com/tft/league/v1/challenger'
# f"https://{platform}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json' 

class StorageError(Exception):
    '''Custom exception for storage-related errors'''
    pass


class GetInformation:
    def __init__(self, column: str, dl_bucket: str, dl_filename: str,  extract_col: int):
        '''This class can take an item from a csv store, then iterate over that file
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

        print('Finished processing')
        return self.result_list

   


class API_caller:
    def __init__(self, search_items: list, region: str, api_endpoint: str, API_KEY, entrypoint_in_return_json: str):
        """Will call a customed api call and then format and store the returning data 
        List of search items is what is being specifically looked at and inserted into the api url query

        Entry point is the json key name of the values you want to retrieve in the table, because
        the JSON from the api is nested and some values are irrelevant, so would have to look
        at data in browser to know what to retrieve
        
        """
        self.search_items = search_items
        self.region = region
        # self.api_endpoint = api_endpoint
        self.api_endpoint = f"https://{region}.api.riotgames.com/{api_endpoint}"
        self.API_KEY = API_KEY
        self.entrypoint = entrypoint_in_return_json

    def make_api_call(self):
        entrypoint = self.entrypoint
        api_endpoint = self.api_endpoint
        search_items = self.search_items
        region = self.region
        api_return_dataframe = pd.DataFrame()
        print(api_return_dataframe)
        print(search_items)
        print('entrypoint=', entrypoint)

        if 'specific' in api_endpoint:
            print('Making api call with customised string')
            count = 0
            for item in search_items:
                count += 1
                if count > 10:
                    break # this iterates of the column extracted prior and inserts into a query string
                # print (api_endpoint.format(region=region, specific=item, API_KEY=API_KEY))
                try:
                    url = api_endpoint.format(region=region, specific=item, API_KEY=API_KEY)
                    response = requests.get(url)
                except requests.exceptions.RequestException as e:
                    print(f"Error making API request: {e}")

                if response.status_code == 200 and entrypoint is not None:
                    response_data = response.json()
                    print(response_data)
                    api_return_dataframe = pd.DataFrame(response_data[entrypoint])

                elif response.status_code == 200:
                    response_data = response.json()
                    res_df = pd.DataFrame(response_data)

                    if api_return_dataframe.empty:
                        api_return_dataframe = pd.DataFrame(response_data)
                    else: api_return_dataframe = pd.concat([api_return_dataframe, res_df], axis=1)

                else:
                    logging.error (response.status_code) # ERROR
                    quit()

        
        
        
        else:
            print ('No specificity defined ')
            print ('Accessing endpoint:', api_endpoint.format(region=region, API_KEY=API_KEY))
            try: 
                url = api_endpoint.format(region=region, API_KEY=API_KEY)
                response = requests.get(url)
            except requests.exceptions.RequestException as e:
                print(f"Error making API request: {e}")

            if response.status_code == 200:
                response_data = response.json()
                api_return_dataframe = pd.DataFrame(response_data[entrypoint])
            else: 
                logging.error (response.status_code)
                quit()
        
            

        print('Returning dataframe')

        return (api_return_dataframe)
    


def csv_store_function(data, file_name):
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
    
    

#  self.api_endpoint = f"https://{region}.api.riotgames.com/{api_endpoint}"

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

