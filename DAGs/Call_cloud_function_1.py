import urllib
import os
import google.auth.transport.requests
import google.oauth2.id_token
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

'''Sends an authorized http request to a google cloud function, invokes the function'''
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/cees/projects_to_work_on/TFT-de-pipeline/Terraform_files/credentials.json'

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
    print(response.read().decode("utf-8"))

    return response.read()

def invoke_cloud_function():
    make_authorized_get_request('https://get-chall-euw-function40-32p4xnt67q-nw.a.run.app', 'https://get-chall-euw-function40-32p4xnt67q-nw.a.run.app')

default_args = {
    'owner': 'cees',
    'start_date': datetime.utcnow(),
}

with DAG(
    'invoke_cloud_function_dag',
    default_args=default_args,
    schedule_interval='*/1 * * * *',
    max_active_runs=1,
    catchup=True,
) as dag:
    invoke_cf = PythonOperator(
        task_id='invoke_cf',
        python_callable=invoke_cloud_function
    )