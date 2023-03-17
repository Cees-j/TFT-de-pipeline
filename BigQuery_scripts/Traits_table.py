from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
import logging

def create_traits_table():
    location = 'europe-west2'
    client = bigquery.Client(location=location)
    job_config = bigquery.QueryJobConfig()  
    

    create_traits_table = """CREATE TABLE `get_chall_euw_dataset_id.traits_data`
    (   match_id STRING,
        participant_id STRING,
        trait_name STRING,  
        num_units INT64,
        style INT64,
        tier_total INT64
    )
    AS ( 
        SELECT
        JSON_EXTRACT_SCALAR(string_field_0, '$.match_id') AS match_id,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.puuid') AS STRING) AS participant_id,
        CAST(JSON_EXTRACT_SCALAR(trait, '$.name') AS STRING) as trait_name,
        CAST(JSON_EXTRACT_SCALAR(trait, '$.tier_total') AS INT64) as tier_total,
        CAST(JSON_EXTRACT_SCALAR(trait, '$.style') AS INT64) as style,
        CAST(JSON_EXTRACT_SCALAR(trait, '$.num_units') AS INT64) as num_units,

    FROM `get_chall_euw_dataset_id.Detailed-data-dump-euw`, 
        UNNEST(JSON_EXTRACT_ARRAY(string_field_1, '$.participants')) AS participant,
        UNNEST(JSON_EXTRACT_ARRAY(participant, '$.traits')) AS trait
    );"""   

    

    insert_traits_data_query = """INSERT INTO `get_chall_euw_dataset_id.traits_data`
    (   match_id,
        participant_id,
        trait_name,
        num_units,
        style,
        tier_total
    )
    SELECT
        JSON_EXTRACT_SCALAR(string_field_0, '$.match_id') AS match_id,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.puuid') AS STRING) AS participant_id,
        CAST(JSON_EXTRACT_SCALAR(trait, '$.name') AS STRING) as trait_name,
        CAST(JSON_EXTRACT_SCALAR(trait, '$.tier_total') AS INT64) as tier_total,
        CAST(JSON_EXTRACT_SCALAR(trait, '$.style') AS INT64) as style,
        CAST(JSON_EXTRACT_SCALAR(trait, '$.num_units') AS INT64) as num_units,
    FROM `get_chall_euw_dataset_id.Detailed-data-dump-euw`, 
        UNNEST(JSON_EXTRACT_ARRAY(string_field_1, '$.participants')) AS participant,
        UNNEST(JSON_EXTRACT_ARRAY(participant, '$.traits')) AS trait
    """

    job = client.query(create_traits_table, job_config=job_config)
    try:
        job.result()
    except Exception as error:
        logging.info(f"An error occurred while executing the query job: {error}, {error.code}")
        job = client.query(insert_traits_data_query, job_config=job_config)
        try:
            job.result()
            logging.info('Inserting instead')
        except Exception as e:
            raise e