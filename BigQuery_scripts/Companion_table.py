from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
import logging


def create_companion_table_job():
    location = 'europe-west2'
    # Set up the BigQuery client and job config
    client = bigquery.Client(location=location)
    job_config = bigquery.QueryJobConfig()

    create_companion_table = """CREATE TABLE `get_chall_euw_dataset_id.companion_data`
    (   match_id STRING,
        participant_id STRING,
        companion_id STRING,
    )
    AS ( 
        SELECT
        JSON_EXTRACT_SCALAR(string_field_0, '$.match_id') AS match_id,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.puuid') AS STRING) AS participant_id,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.companion.content_ID') AS STRING) AS companion_id
    FROM `get_chall_euw_dataset_id.Detailed-data-dump-euw`, 
        UNNEST(JSON_EXTRACT_ARRAY(string_field_1, '$.participants')) AS participant,
        UNNEST(JSON_EXTRACT_ARRAY(participant, '$.traits')) AS trait
    );"""

    insert_companion_table = """INSERT INTO `get_chall_euw_dataset_id.companion_data`
    (   match_id,
        participant_id, 
        companion_id 
    )
        SELECT
        JSON_EXTRACT_SCALAR(string_field_0, '$.match_id') AS match_id,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.puuid') AS STRING) AS participant_id,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.companion.content_ID') AS STRING) AS companion_id
    FROM `get_chall_euw_dataset_id.Detailed-data-dump-euw`, 
        UNNEST(JSON_EXTRACT_ARRAY(string_field_1, '$.participants')) AS participant,
        UNNEST(JSON_EXTRACT_ARRAY(participant, '$.traits')) AS trait
    ;"""   

    job = client.query(create_companion_table, job_config=job_config)
    try: 
        job.result()
    except Exception as error:
        logging.info(f"An error occurred while executing the query job: {error}, {error.code}")
        job = client.query(insert_companion_table, job_config=job_config)
        try:
            job.result()
            logging.info('Inserting instead')
        except Exception as e:
            raise e