from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
import os
import json
import google.oauth2.id_token
import google.auth.transport.requests

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gs://europe-west2-euw2-json-test-8118d3f5-bucket/dags/json-test-377211-4a170a2a7d54.json' # upload json file to composer dag directory  
# print(os.environ)
# request = google.auth.transport.requests.Request()
# audience = 'https://get-chall-function2-32p4xnt67q-nw.a.run.app' #'https://mylocation-myprojectname.cloudfunctions.net/MyFunctionName'
# TOKEN = google.oauth2.id_token.fetch_id_token(request, audience)


# should be able to dorp this in composer dag file and then can make it run every 3 mins 
default_args = {
    'owner': 'Cees',
    'start_date': datetime.utcnow(),
    'email': ['ceesjdu@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'send_http_request_EUW_chall_function',
    default_args=default_args,
    schedule_interval='*/1 * * * *',
    max_active_runs=1
)

send_http_request = SimpleHttpOperator(
    task_id='send_http_request',
    method='GET',
    http_conn_id='123json321_CHALL_GET',
    dag=dag
)
