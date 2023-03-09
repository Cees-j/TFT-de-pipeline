from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
import logging

def create_match_data_table_job():

    location = 'europe-west2'
    # Set up the BigQuery client and job config
    client = bigquery.Client(location=location)
    job_config = bigquery.QueryJobConfig()

    create_match_data_table = """
    CREATE TABLE `get_chall_euw_dataset_id.match_data`
    (
        match_id STRING,
        game_datetime INT64,
        game_length FLOAT64,
        game_version STRING,

    )
    AS (
        SELECT 
            JSON_EXTRACT_SCALAR(string_field_0, '$.match_id')  AS match_id,
            CAST(JSON_EXTRACT_SCALAR(string_field_1, '$.game_datetime') AS INT64) AS game_datetime,
            CAST(JSON_EXTRACT_SCALAR(string_field_1, '$.game_length') AS FLOAT64) AS game_length,
            JSON_EXTRACT_SCALAR(string_field_1, '$.game_version') AS game_version
        FROM `get_chall_euw_dataset_id.Detailed-data-dump-euw`
    );
    """ 

    insert_match_data = """
    INSERT INTO `get_chall_euw_dataset_id.match_data`
    (
        match_id,
        game_datetime,
        game_length,
        game_version 

    )
    AS (
        SELECT 
            JSON_EXTRACT_SCALAR(string_field_0, '$.match_id')  AS match_id,
            CAST(JSON_EXTRACT_SCALAR(string_field_1, '$.game_datetime') AS INT64) AS game_datetime,
            CAST(JSON_EXTRACT_SCALAR(string_field_1, '$.game_length') AS FLOAT64) AS game_length,
            JSON_EXTRACT_SCALAR(string_field_1, '$.game_version') AS game_version
        FROM `get_chall_euw_dataset_id.Detailed-data-dump-euw`
    );
    """ 
    print('Starting query to create table')
    job = client.query(create_match_data_table, job_config=job_config)
    try: 
        job.result()
    except Exception as error:
        logging.info(f"An error occurred while executing the query job: {error}, {error.code}")
        job = client.query(insert_match_data, job_config=job_config)
        try:
            job.result()
            logging.info('Inserting instead')
        except Exception as e:
            raise e

def delete_unnecessary_job():
    location = 'europe-west2'
    # Set up the BigQuery client and job config
    client = bigquery.Client(location=location)
    job_config = bigquery.QueryJobConfig()

    delete_unnecessary = """
    DELETE FROM `get_chall_euw_dataset_id.match_data`
    WHERE match_id IS NULL;
    """

    job = client.query(delete_unnecessary, job_config=job_config)
    try: 
        job.result()
    except GoogleAPIError as error:
        print(f"An error occurred while executing the query job: {error}")