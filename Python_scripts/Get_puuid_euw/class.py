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
    def __init__(self, column, dl_bucket, dl_filename,  extract_col):
        '''This class can take an item from a csv store, then iterate over that file
        and take whichever column it is you need from the csv, and store that in a list, which 
        can then be given to another class to make api calls.'''

        self.column = column
        self.download_bucket = dl_bucket
        self.download_filename = dl_filename
        self.extract_col = extract_col
        self.result_list = []


    def process_csv_file(self, csv_reader): 
        print('processing file')
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
                print(extracted_row)
                self.result_list.append(extracted_row)
                # result = api_call(puuid)
        

    def download_csv_file(self):
        print('downloading file')
        file_name = self.download_filename
        
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.download_bucket)
        blob = bucket.blob(file_name)
        contents = blob.download_as_string().decode('utf-8')

        csv_reader = csv.reader(contents.split('\n'))
        self.process_csv_file(csv_reader)
        return csv_reader

    def make_api_call(self):
        pass

info = GetInformation('puuid', 'csv-store-10001', 'Get_PUUID_euw.csv', 2)

info.download_csv_file()
print(info.result_list)

#  self.api_endpoint = f"https://{region}.api.riotgames.com/{api_version}"
