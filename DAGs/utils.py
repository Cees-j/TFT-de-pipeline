import logging
import urllib
import os
import google.auth.transport.requests
import google.oauth2.id_token
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from google.cloud import bigquery


def make_authorized_get_request(endpoint, audience):
    """
    make_authorized_get_request makes a GET request to the specified HTTP endpoint
    by authenticating with the ID token obtained from the google-auth client library
    using the specified audience value.
    """
    print('Making request to', endpoint)

    # Cloud Functions uses your function's URL as the `audience` value
    # audience = https://project-region-projectid.cloudfunctions.net/myFunction
    # For Cloud Functions, `endpoint` and `audience` should be equal

    req = urllib.request.Request(endpoint)

    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    req.add_header("Authorization", f"Bearer {id_token}")
    response = urllib.request.urlopen(req)
    print('Response received: ', response.read().decode("utf-8"))

    return response.read()

def invoke_cloud_func(url, url2):
    make_authorized_get_request(url, url2)


project_id = 'json-test-377211'
dataset_id = 'get_chall_euw_dataset_id'
json_dump_table = 'Detailed-data-dump-euw'
match_table = 'match_data'

def print_true():
    print("Table exists")

def print_false():
    print("Table does not exist")

def check_table_existence(project_id, dataset_id, table_id, **kwargs):
    '''This checks if a table exists, if it doesnt, log the exception and return False
    otherwise retunr True and log table'''
    try:
        client = bigquery.Client(project=project_id)
        table_ref = client.dataset(dataset_id).table(table_id)
        table = client.get_table(table_ref)
        print('got table', table)
        return True
    except Exception as e:
        print('exception printing!!!:::', e)
        if "Not found: Table" in str(e):
            return False
        else:
            raise e