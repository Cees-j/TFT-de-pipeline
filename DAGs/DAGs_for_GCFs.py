import urllib
import os
import google.auth.transport.requests
import google.oauth2.id_token
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.gcs_sensor import GCSObjectExistenceSensor
from python_utils import make_authorized_get_request, invoke_cloud_func
import logging

'''Sends an authorized http request to a google cloud function, invokes the function'''

default_args = {
    'owner': 'cees',
    'start_date': datetime.utcnow(),
}

with DAG(
    'invoke_cloud_function_dag_plus_utils',
    default_args=default_args,
    schedule_interval='*/55 * * * *',
    max_active_runs=1,
    catchup=True,
) as dag:
    invoke_cf = PythonOperator(
        task_id='get_euw_chall',
        python_callable=invoke_cloud_func,
        op_kwargs={'url': 'https://get-chall-euw-function40-32p4xnt67q-nw.a.run.app',
                   'url2': 'https://get-chall-euw-function40-32p4xnt67q-nw.a.run.app' }
    )

    wait_for_euw_chall_file = GCSObjectExistenceSensor(
        task_id='wait_for_euw_chall',
        bucket='csv-store-10001',
        object='euw_chall.csv'
    )   

    invoke_cf_2 = PythonOperator(
        task_id='get_euw_puuid',
        python_callable=invoke_cloud_func,
        op_kwargs={'url': 'https://get-puuid-euw-function40-32p4xnt67q-nw.a.run.app',
                   'url2': 'https://get-puuid-euw-function40-32p4xnt67q-nw.a.run.app' }
    )

    wait_for_euw_puuid_file = GCSObjectExistenceSensor(
        task_id='wait_for_euw_puuid',
        bucket='csv-store-10001',
        object='sailmate'
    )   

    invoke_cf_3 = PythonOperator(
        task_id='get_euw_matches',
        python_callable=invoke_cloud_func,
        op_kwargs={'url': 'https://get-matches-euw-function40-32p4xnt67q-nw.a.run.app',
                   'url2': 'https://get-matches-euw-function40-32p4xnt67q-nw.a.run.app' }
    )

    wait_for_euw_matches_data = GCSObjectExistenceSensor(
        task_id='wait_for_euw_matches',
        bucket='csv-store-10001',
        object='sailmate2'
    )   

    invoke_cf_4 = PythonOperator(
        task_id='get_euw_detailed_matches',
        python_callable=invoke_cloud_func,
        op_kwargs={'url': 'https://get-detailed-matches-euw-function41-32p4xnt67q-nw.a.run.app',
                   'url2': 'https://get-detailed-matches-euw-function41-32p4xnt67q-nw.a.run.app' }
    )

    invoke_cf >> wait_for_euw_chall_file >> invoke_cf_2 >> wait_for_euw_puuid_file >> invoke_cf_3 >> wait_for_euw_matches_data >> invoke_cf_4