# Data Engineering Project ( Work In Progress ) 
This is a data engineering project that retrieves data from an API, transforms it, and loads it into BigQuery using a set of Python scripts. The project is designed to use Cloud Functions for retrieving and transforming data, and to run in GCP Cloud Composer, an Apache Airflow-based workflow orchestration service. The infrastructure for the project is provisioned using Terraform.

# Project Structure
The project consists of the following files and directories:

Python_scripts/: Directory containing the Python scripts for retrieving and transforming data. <br>
DAGs/: Directory containing the Airflow DAG definition file for scheduling the Python scripts to run. <br>
requirements.txt: File containing the Python package dependencies for the project. <br>
Terraform_files/: Directory containing the Terraform configuration files for provisioning the cloud infrastructure. <br>

# Setup
To set up the project, follow these steps:

TBC 

# Dependencies
The project relies on the following Python packages, which are specified in the requirements.txt file:

google-cloud-bigquery <br>
requests <br>
pandas <br>
google-cloud-storage <br>
google-auth <br>
google-cloud-bigquery <br>



# Data warehouse schema
| Column Name       | Data Type | Constraints               |
|-------------------|----------|---------------------------|
| match_id          | integer  | primary key               |
| game_datetime     | datetime |                           |
| game_length       | integer  |                           |
| game_version      | string   |                           |
| participant_id    | integer  | primary key, foreign key   |
| puuid             | string   |                           |
| gold_left         | integer  |                           |
| last_round        | integer  |                           |
| level             | integer  |                           |
| placement         | integer  |                           |
| players_eliminated| integer  |                           |
| time_eliminated   | integer  |                           |
| total_damage_to_players | integer |                   |
| trait_id          | integer  | primary key               |
| name              | string   |                           |
| num_units         | integer  |                           |
| style             | string   |                           |
| tier_current      | integer  |                           |
| tier_total        | integer  |                           |
| unit_id           | integer  | primary key               |
| character_id      | string   |                           |
| itemNames         | string   |                           |
| items             | string   |                           |
| name              | string   |                           |
| rarity            | string   |                           |
| tier              | integer  |                           |
| companion_id      | integer  | primary key               |
| content_ID        | string   |                           |
| item_ID           | string   |                           |
| skin_ID           | string   |                           |
| species           | string   |                           |
Data Warehouse Schema
Table: Game
Column Name	Data Type	Constraints
match_id	integer	primary key
game_datetime	datetime	
game_length	integer	
game_version	string	
Table: Participant
Column Name	Data Type	Constraints
participant_id	integer	primary key
match_id	integer	foreign key to Game
puuid	string	
gold_left	integer	
last_round	integer	
level	integer	
placement	integer	
players_eliminated	integer	
time_eliminated	integer	
total_damage_to_players	integer	
Table: Trait
Column Name	Data Type	Constraints
trait_id	integer	primary key
participant_id	integer	foreign key to Participant
name	string	
num_units	integer	
style	string	
tier_current	integer	
tier_total	integer	
Table: Unit
Column Name	Data Type	Constraints
unit_id	integer	primary key
participant_id	integer	foreign key to Participant
character_id	string	
itemNames	string	
items	string	
name	string	
rarity	string	
tier	integer	
Table: Companion
Column Name	Data Type	Constraints
companion_id	integer	primary key
participant_id	integer	foreign key to Participant
content_ID	string	
item_ID	string	
skin_ID	string	
species	string	
This data warehouse schema represents the database schema for game information related to a match. The database consists of five tables, Game, Participant, Trait, Unit, and Companion.

The Game table stores general information about the game, including the match_id, game_datetime, game_length, and game_version.

The Participant table stores information about each participant in the match, including the participant_id, match_id, puuid, gold_left, last_round, level, placement, players_eliminated, time_eliminated, and total_damage_to_players.

The Trait table stores information about the traits of each participant in the game. It includes the trait_id, participant_id, name, num_units, style, tier_current, and tier_total.

The Unit table stores information about each unit in the game. It includes the unit_id, participant_id, character_id, itemNames, items, name, rarity, and tier.

The Companion table stores information about the companions of each participant in the game. It includes the companion_id, participant_id, content_ID, item_ID, skin_ID, and species.

This data warehouse schema shows how these tables are related to each other using the match_id and participant_id columns. The match_id column serves as a foreign key in Participant, Trait, Unit, and Game tables, linking them together. The participant_id column is used to identify the individual participants within each match and serves as a foreign key in Trait, Unit, Companion, and `Participant




