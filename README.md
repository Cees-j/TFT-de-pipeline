# Data Engineering Project ( Work In Progress ) 
This is a data engineering project that retrieves data from an API, transforms it, and loads it into BigQuery using a set of Python scripts. The project is designed to use Cloud Functions for retrieving and transforming data, and to run in GCP Cloud Composer, an Apache Airflow-based workflow orchestration service. The infrastructure for the project is provisioned using Terraform.

# Project Structure
The project consists of the following files and directories:

Python_scripts/: Directory containing the Python scripts for retrieving and transforming data. <br>
DAGs/: Directory containing the Airflow DAG definition file for scheduling the Python scripts to run. <br>
Terraform_files/: Directory containing the Terraform configuration files for provisioning the cloud infrastructure. <br>
BigQuery_scripts/: Directory containing python scripts for creating BigQuery tables. <br>



# Data warehouse schema
### Table: match_data

| Column Name   | Data Type | Constraints  |
|---------------|-----------|--------------|
| match_id      | integer   | primary key  |
| game_datetime | datetime  |              |
| game_length   | integer   |              |
| game_version  | string    |              |

### Table: game_results

| Column Name         | Data Type | Constraints              |
|---------------------|-----------|--------------------------|
| participant_id      | integer   | primary key              |
| match_id            | integer   | foreign key to match_data|
| total_damage_to_players| integer|                          |
| players_eliminated  | integer   |                          |
| placement           | integer   |                          |
| gold_left           | integer   |                          |
| last_round          | integer   |                          |
| game_length         | integer   |                          |
| level               | integer   |                          |


### Table: traits_data

| Column Name     | Data Type | Constraints                      |
|-----------------|-----------|----------------------------------|
| match_id        | integer   | foreign key to match_data        |
| participant_id  | integer   | foreign key to game_results      |
| trait_name      | string    |                                  |
| num_units       | integer   |                                  |
| style           | string    |                                  |
| tier_total      | integer   |                                  |

### Table: units_per_player_and_match

| Column Name      | Data Type | Constraints                   |
|------------------|-----------|-------------------------------|
| match_id         | integer   | foreign key to match_data     |
| participant_id   | integer   | foreign key to game_results   |
| unit_id          | string    |                               |
| rarity           | string    |                               |
| tier             | integer   |                               |
| itemNames        | string    |                               |

### Table: companion_data

| Column Name      | Data Type | Constraints                   |
|------------------|-----------|-------------------------------|
| match_id         | integer   | foreign key to match_data     |
| participant_id   | integer   | foreign key to game_results   |
| companion_id     | string    |                               |



This data warehouse schema represents the database schema for game information related to a match. The database consists of five tables:

The match_data table stores general information about the match, including the match_id, game_datetime, game_length, and game_version.

The game_results table stores information about each participant in the match, including the participant_id, match_id, puuid, gold_left, last_round, level, placement, players_eliminated, time_eliminated, and total_damage_to_players.

The traits_data table stores information about the traits of each participant in the game. It includes the match_id, participant_id, trait_name, num_units, style, and tier_total.

The units_per_player_and_match table stores information about each unit in the game. It includes the match_id, participant_id, unit_id, rarity, tier, and itemNames.

The companion_data table stores information about the companions of each participant in the game. It includes the match_id, participant_id, and companion_id.

The composite keys of match and participant id are necessary due to each match id having 8 possible participants. By using composite keys, the schema allows for easy linking of data between the different tables based on the match and participant. This allows for complex queries and analysis of the game data to be performed efficiently.



