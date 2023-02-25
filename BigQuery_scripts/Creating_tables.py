from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"
location = 'europe-west2'
# Set up the BigQuery client and job config
client = bigquery.Client(location=location)
job_config = bigquery.QueryJobConfig()



# Extracts meta data
# query = """
# CREATE TABLE get_chall_euw_dataset_id.destination_table
# AS (
#   SELECT JSON_EXTRACT_SCALAR(string_field_0, '$.data_version') AS data_version,
#          JSON_EXTRACT_SCALAR(string_field_0, '$.match_id') AS match_id,
#          JSON_EXTRACT_ARRAY(string_field_0, '$.participants') AS participants
#   FROM `get_chall_euw_dataset_id.Detailed-data-dump-euw`
# )
# """


# job = client.query(query, job_config=job_config)
# job.result()
# for row in job.result():
#     print(row)

############################################################################

# first drill down into info
first_info_drill_query = """ 
CREATE TABLE get_chall_euw_dataset_id.dest2
AS (
    SELECT JSON_EXTRACT_SCALAR(string_field_0, '$.game_datetime') AS game_datetime,
        JSON_EXTRACT_SCALAR(string_field_0, '$.game_length') AS game_length,
        JSON_EXTRACT_SCALAR(string_field_0, '$.game_version') AS game_version,
        JSON_EXTRACT_ARRAY(string_field_1, '$.participants') AS overall_data
    FROM `get_chall_euw_dataset_id.Detailed-data-dump-euw`
)
"""
first_info_drill_query_job = client.query(first_info_drill_query, job_config=job_config)
first_info_drill_query_job.result()

############################################################################