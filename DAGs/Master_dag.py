from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from utils import project_id, dataset_id, match_table, print_true, print_false, check_table_existence
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from Match_data2 import create_match_data_table_job, delete_unnecessary_job
from google.cloud import bigquery
import urllib
import os
import google.auth.transport.requests
import google.oauth2.id_token
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.gcs_sensor import GCSObjectExistenceSensor
from utils import make_authorized_get_request, invoke_cloud_func
from airflow.utils.task_group import TaskGroup
import logging

default_args = {
    'retries': 0
}

with DAG(
    dag_id='Big_dag2',
    start_date=datetime.now(),
    schedule_interval='@once',  
    default_args=default_args
) as DAG:

    with TaskGroup('extraction_cloud_function_tasks') as extraction_cloud_function_tasks:
        invoke_cf = PythonOperator(
            task_id='get_euw_chall',
            python_callable=invoke_cloud_func,
            op_kwargs={'url': 'https://get-chall-euw-function40-32p4xnt67q-nw.a.run.app',
                        'url2': 'https://get-chall-euw-function40-32p4xnt67q-nw.a.run.app' },
        )

        wait_for_euw_chall_file = GCSObjectExistenceSensor(
            task_id='wait_for_euw_chall',
            bucket='csv-store-10001',
            object='euw_chall.csv',
        )   

        invoke_cf_2 = PythonOperator(
            task_id='get_euw_puuid',
            python_callable=invoke_cloud_func,
            op_kwargs={'url': 'https://get-puuid-euw-function40-32p4xnt67q-nw.a.run.app',
                        'url2': 'https://get-puuid-euw-function40-32p4xnt67q-nw.a.run.app' },
        )

        wait_for_euw_puuid_file = GCSObjectExistenceSensor(
            task_id='wait_for_euw_puuid',
            bucket='csv-store-10001',
            object='sailmate',
        )   

        invoke_cf_3 = PythonOperator(
            task_id='get_euw_matches',
            python_callable=invoke_cloud_func,
            op_kwargs={'url': 'https://get-matches-euw-function40-32p4xnt67q-nw.a.run.app',
                        'url2': 'https://get-matches-euw-function40-32p4xnt67q-nw.a.run.app' },
        )

        wait_for_euw_matches_data = GCSObjectExistenceSensor(
            task_id='wait_for_euw_matches',
            bucket='csv-store-10001',
            object='sailmate2',
        )   

        invoke_cf_4 = PythonOperator(
            task_id='get_euw_detailed_matches',
            python_callable=invoke_cloud_func,
            op_kwargs={'url': 'https://get-detailed-matches-euw-function41-32p4xnt67q-nw.a.run.app',
                        'url2': 'https://get-detailed-matches-euw-function41-32p4xnt67q-nw.a.run.app' },
        )



    check_match_table_existence = PythonOperator(
        task_id='check_match_table_existence', 
        python_callable=check_table_existence,
        provide_context=True,
        op_kwargs={'project_id': project_id, 'dataset_id': dataset_id, 'table_id': match_table},
    )

    branch_task = BranchPythonOperator(
        task_id='branch_task',
        provide_context=True,
        # This line below check if the xcom pull from checking is true.
        python_callable=lambda ti: 'true_task' if ti.xcom_pull(task_ids='check_match_table_existence') else 'false_task',
    )

    true_task = PythonOperator(
        task_id='true_task',
        python_callable=print_true,
    )

    create_match_data_table_task = PythonOperator(
        task_id="create_match_data_table",
        python_callable=create_match_data_table_job,
    )

    delete_unnecessary_task = PythonOperator(
        task_id="delete_unnecessary",
        python_callable=delete_unnecessary_job,
    )
    false_task = PythonOperator(
        task_id='false_task',
        python_callable=print_false,
    )

    dummy_task1 = DummyOperator(
        task_id="dummy_task1",
        trigger_rule="all_done"
    )

(invoke_cf >> wait_for_euw_chall_file >> invoke_cf_2 >> wait_for_euw_puuid_file >> 
    invoke_cf_3 >> wait_for_euw_matches_data >> invoke_cf_4)
    
extraction_cloud_function_tasks >> check_match_table_existence >> branch_task

branch_task >> true_task >> dummy_task1
branch_task >> false_task >> create_match_data_table_task >> delete_unnecessary_task >> dummy_task1
