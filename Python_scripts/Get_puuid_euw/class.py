import csv
import requests
from google.cloud import storage
import pandas as pd
from api_key import API_KEY
import os
# f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={API_KEY}"
# f'https://{region}.api.riotgames.com/tft/league/v1/challenger'
# f"https://{platform}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json' 
class GetInformation:
    def __init__(self, api_version, column, dl_bucket, dl_filename, region, extract_col):
        '''This class can take an item from a csv store, then iterate over that file and make an
        api call based on a row in the csv. Then from that api call it will store a csv'''
        self.api_version = api_version
        self.column = column
        self.download_bucket = dl_bucket
        self.download_filename = dl_filename
        self.region = region
        self.extract_col = extract_col

        self.api_endpoint = f"https://{region}.api.riotgames.com/{api_version}"

    def process_csv_file(self):
        print('downloading file')
        file_name = self.download_filename
        extract_col = self.extract_col
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.download_bucket)
        blob = bucket.blob(file_name)
        contents = blob.download_as_string().decode('utf-8')

        reader = csv.reader(contents.split('\n'))
        next(reader)    

        count = 0
        for row in reader:
            count += 1
            if count > 25:
                break
            if len(row)>2:
                extracted_row = row[extract_col]
                print(extracted_row)
                # result = api_call(puuid)

    def make_api_call(self):
        pass

info = GetInformation("lol/summoner/v4/summoners/by-name/{name}?api_key={API_KEY}",
                      'puuid', 'csv-store-10001', 'Get_PUUID_euw.csv', 'euw1', 2)

info.process_csv_file()
    # def get_data(self, filter_func=None):
    #     with open(self.csv_filename, 'r') as csv_file:
    #         csv_reader = csv.reader(csv_file)
    #         headers = next(csv_reader)  # read the header row

    #         if not 'puuid' in headers:
    #             raise ValueError('CSV file must contain a column called "puuid"')

    #         data = []
    #         for row in csv_reader:
    #             if filter_func and not filter_func(row):
    #                 continue

    #             puuid = row[headers.index('puuid')]
    #             url = f'{self.api_endpoint}/{puuid}'
    #             response = requests.get(url)

    #             if response.status_code == 200:
    #                 data.append(response.json())
    #             else:
    #                 print(f'Error {response.status_code} for puuid {puuid}')

    #     return data
    
