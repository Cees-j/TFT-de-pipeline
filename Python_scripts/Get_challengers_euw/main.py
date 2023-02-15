import pandas as pd
import requests
from google.cloud import storage
from google.oauth2.service_account import Credentials
import logging

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-f3d7190e-9971-4027-9b31-bddfd5c3666d" # API KEY HERE
} 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.info('Get Chall Script Initialized')

class StorageError(Exception):
    '''Custom exception for storage-related errors'''
    pass

def store_csv(data):
    '''Will take the formatted get_chall dataframe and store it in the bucket called csv-store'''
    try:
        storage_client = storage.Client()
        bucket_name = 'csv-store-10001'
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob('Get_chall_euw.csv')
        blob.upload_from_string(data)
        logging.info(f'Get_chall_euw stored in {bucket_name}')
        return 'Csv EUW Complete'
    except Exception as e:
        raise StorageError(f"Failed to store CSV data: {str(e)}")


def get_chall_ladder_data(r):
    region = 'euw1'
    logging.info(f"this is what is being passed {r}")
    '''Makes a request to an api based on region, if code is 200 then continues on to format the incoming
    data and changes it into a csv to be passed into the storage function'''
    
    chall_response = requests.get(f'https://{region}.api.riotgames.com/tft/league/v1/challenger', headers=headers)
    if chall_response.status_code != 200:
        logger.error(f"HTTP error {chall_response.status_code} occurred, {region}")
        raise requests.exceptions.HTTPError(chall_response.status_code) 

    chall_data = chall_response.json()
    challenger_df = pd.DataFrame(chall_data['entries'])
    challenger_df.drop(columns=['veteran', 'freshBlood'], axis=1, inplace=True)

    csv_data = challenger_df.to_csv(index=False)

    print(f'Success - acquired challenger ladder for {region}')

    store_csv(csv_data)


