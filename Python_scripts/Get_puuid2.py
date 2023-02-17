import os
import csv
import requests
from google.cloud import storage
print("Current working directory: ", os.getcwd())
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json'

empty = []
def api_call(name):
    empty.append(name)

    # Make an API call for a single name
    # response = requests.get(f'https://example.com/api/name/{name}')
    # if response.status_code == 200:
    #     return response.json()
    # else:
    #     return None

def process_csv_file(bucket_name, file_name):
    # Download the CSV file from Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    contents = blob.download_as_string().decode('utf-8')



    # Parse the CSV file and sort by leaguePoints in descending order
    reader = csv.reader(contents.split('\n'))
    header = next(reader)  # get the header row
    data = list(reader) 
    data_sorted = sorted(data, key=lambda row: int(row[2]) if len(row) >= 3 else 0, reverse=True) # sort by leaguePoints
    

    # Make an API call for each name, will do 50 names at a time for rate limit purposes
    count = 0
    for row in data_sorted:
        count += 1
        if count == 50:
            break
        if len(row) > 0:
            name = row[1]
            if name == 'summonerName':
                continue
            result = api_call(name)
    
            # print(result)  # Replace this with your desired logging or storage operation
    print(empty)

def my_cloud_function(event, context):
    # Triggered by a new file in a Cloud Storage bucket
    bucket_name = event['bucket']
    file_name = event['name']
    process_csv_file(bucket_name, file_name)

process_csv_file('csv-store-10001', 'Get_chall_euw.csv')