from google.cloud import bigquery

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
    try:
        print('Starting query to create table')
        client.query(create_match_data_table, job_config=job_config)
        print('Query finished, table created')
    except Exception as e:
        print(f'Error creating table: {str(e)}')
        raise e
    #client.query(create_match_data_table, job_config=job_config)

def delete_unnecessary_job():
    location = 'europe-west2'
    # Set up the BigQuery client and job config
    client = bigquery.Client(location=location)
    job_config = bigquery.QueryJobConfig()

    delete_unnecessary = """
    DELETE FROM `get_chall_euw_dataset_id.match_data`
    WHERE match_id IS NULL;
    """

    client.query(delete_unnecessary, job_config=job_config)