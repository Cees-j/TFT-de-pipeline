from google.cloud import bigquery
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"
location = 'europe-west2'
# Set up the BigQuery client and job config
client = bigquery.Client(location=location)
job_config = bigquery.QueryJobConfig()


# Creates the results of match, one match id and 8 participant ids, each with theyre own data
create_match_results_table = """CREATE TABLE get_chall_euw_dataset_id.game_results2 (
    match_id STRING,
    participant_id STRING,
    total_damage_to_players INT64,
    players_eliminated INT64,
    placement INT64,
    gold_left INT64,
    last_round INT64,
    game_length FLOAT64,
    level INT64,
)
AS (
    SELECT 
        JSON_EXTRACT_SCALAR(string_field_0, '$.match_id') AS match_id,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.puuid') AS STRING) AS participant_id,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.total_damage_to_players') AS INT64) AS total_damage_to_players,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.players_eliminated') AS INT64) AS players_eliminated,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.placement') AS INT64) AS placement,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.gold_left') AS INT64) AS gold_left,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.last_round') AS INT64) AS last_round,
        CAST(JSON_EXTRACT_SCALAR(string_field_1, '$.game_length') AS FLOAT64) AS game_length,
        CAST(JSON_EXTRACT_SCALAR(participant, '$.level') AS INT64) AS level,
    FROM `get_chall_euw_dataset_id.Detailed-data-dump-euw`,
         UNNEST(JSON_EXTRACT_ARRAY(string_field_1, '$.participants')) AS participant
);
"""

create_match_results_table_job = client.query(create_match_results_table, job_config=job_config)
# create_match_results_table_job.result()

# Splits out data further so that match and participant id now splits into units aswell.
# So that you can isolate a match and a participant and the units that they are playing, on
# the assumption that both player id and match id need to be unique
create_units_by_player_and_match_query = """CREATE TABLE get_chall_euw_dataset_id.units_per_player_and_match (
    match_id STRING,
    participant_id STRING,
    unit_id STRING,
    rarity INT64,
    tier INT64,
    item_names STRING
)
AS (
    SELECT
JSON_EXTRACT_SCALAR(string_field_0, '$.match_id') AS match_id,
CAST(JSON_EXTRACT_SCALAR(participant, '$.puuid') AS STRING) AS participant_id,
CAST(JSON_EXTRACT_SCALAR(unit, '$.character_id') AS STRING) AS unit_id,
CAST(JSON_EXTRACT_SCALAR(unit, '$.rarity') AS INT64) AS rarity,
CAST(JSON_EXTRACT_SCALAR(unit, '$.tier') AS INT64) AS star,
JSON_EXTRACT(unit, '$.itemNames') AS item_names
FROM `get_chall_euw_dataset_id.Detailed-data-dump-euw`,
     UNNEST(JSON_EXTRACT_ARRAY(string_field_1, '$.participants')) AS participant,
     UNNEST(JSON_EXTRACT_ARRAY(participant, '$.units')) AS unit
);
"""

create_units_by_player_and_match_query_job = client.query(create_units_by_player_and_match_query, job_config=job_config)
create_units_by_player_and_match_query_job.result()
