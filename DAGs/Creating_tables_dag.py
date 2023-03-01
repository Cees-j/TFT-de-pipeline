from datetime import datetime
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from variables import project_id, dataset_id, match_table
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from Match_data2 import create_match_data_table_job, delete_unnecessary_job
from google.cloud import bigquery

DAG = DAG(
  dag_id='example_dag34',
  start_date=datetime.now(),
  schedule_interval='@once'
)

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
        
check_match_table_existence = PythonOperator(
    task_id='check_match_table_existence', 
    python_callable=check_table_existence,
    provide_context=True,
    op_kwargs={'project_id': project_id, 'dataset_id': dataset_id, 'table_id': match_table},
    dag=DAG)

# def pull_function(**kwargs):
#     '''Pulls the return value of a task'''
#     ti = kwargs['ti']
#     return_value = ti.xcom_pull(task_ids='check_match_table_existence')
#     print(return_value)

# pull_task2 = PythonOperator(
#     task_id='pull_task2', 
#     python_callable=pull_function,
#     provide_context=True,
#     dag=DAG)
# #####
branch_task = BranchPythonOperator(
    task_id='branch_task',
    provide_context=True,
    # This line below check if the xcom pull from checking is true.
    python_callable=lambda ti: 'true_task' if ti.xcom_pull(task_ids='check_match_table_existence') else 'false_task',
    dag=DAG,
)

true_task = PythonOperator(
    task_id='true_task',
    python_callable=print_true,
    dag=DAG,
)

create_match_data_table_task = PythonOperator(
    task_id="create_match_data_table",
    python_callable=create_match_data_table_job,
    dag=DAG,
)

delete_unnecessary_task = PythonOperator(
    task_id="delete_unnecessary",
    python_callable=delete_unnecessary_job,
    dag=DAG,
)

false_task = PythonOperator(
    task_id='false_task',
    python_callable=print_false,
    dag=DAG,
)

dummy_task1 = DummyOperator(
    task_id="dummy_task1",
    dag=DAG,
)




check_match_table_existence >> branch_task

branch_task >> true_task >> dummy_task1
branch_task >> false_task >> create_match_data_table_task >> delete_unnecessary_task >> dummy_task1
