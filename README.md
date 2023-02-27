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

Table: Game
- match_id (primary key)
- game_datetime
- game_length
- game_version

Table: Participant
- participant_id (primary key)
- match_id (foreign key to Game)
- puuid
- gold_left
- last_round
- level
- placement
- players_eliminated
- time_eliminated
- total_damage_to_players

Table: Trait
- trait_id (primary key)
- participant_id (foreign key to Participant)
- name
- num_units
- style
- tier_current
- tier_total

Table: Unit
- unit_id (primary key)
- participant_id (foreign key to Participant)
- character_id
- itemNames
- items
- name
- rarity
- tier

Table: Companion
- companion_id (primary key)
- participant_id (foreign key to Participant)
- content_ID
- item_ID
- skin_ID
- species

Table: ParticipantTrait
- participant_id (composite primary key with trait_id)
- trait_id (composite primary key with participant_id)

Table: ParticipantUnit
- participant_id (composite primary key with unit_id)
- unit_id (composite primary key with participant_id)




-- Fact table: Game Results
CREATE TABLE game_results (
    match_id INT NOT NULL,
    total_damage_to_players INT,
    players_eliminated INT,
    placement INT,
    gold_left INT,
    last_round INT,
    game_length INT,
    num_units INT,
    num_traits INT,
    PRIMARY KEY (match_id)
);

-- Dimension table: Match
CREATE TABLE match (
    match_id INT PRIMARY KEY,
    game_datetime DATETIME,
    game_version VARCHAR(50)
);

-- Dimension table: Participant
CREATE TABLE participant (
    participant_id INT PRIMARY KEY,
    match_id INT,
    puuid VARCHAR(50),
    time_eliminated INT,
    level INT,
    FOREIGN KEY (match_id) REFERENCES match(match_id)
);

-- Dimension table: Unit
CREATE TABLE unit (
    unit_id INT PRIMARY KEY,
    participant_id INT,
    character_id VARCHAR(50),
    item_names VARCHAR(100),
    items VARCHAR(100),
    name VARCHAR(50),
    rarity INT,
    tier INT,
    FOREIGN KEY (participant_id) REFERENCES participant(participant_id)
);

-- Dimension table: Trait
CREATE TABLE trait (
    trait_id INT PRIMARY KEY,
    name VARCHAR(50),
    style VARCHAR(50),
    tier_current INT,
    tier_total INT
);

-- Dimension table: Companion
CREATE TABLE companion (
    companion_id INT PRIMARY KEY,
    participant_id INT,
    content_id VARCHAR(50),
    item_id VARCHAR(50),
    skin_id VARCHAR(50),
    species VARCHAR(50),
    FOREIGN KEY (participant_id) REFERENCES participant(participant_id)
);

-- Bridge table: Participant Trait
CREATE TABLE participant_trait (
    participant_id INT,
    trait_id INT,
    PRIMARY KEY (participant_id, trait_id),
    FOREIGN KEY (participant_id) REFERENCES participant(participant_id),
    FOREIGN KEY (trait_id) REFERENCES trait(trait_id)
);

-- Bridge table: Participant Unit
CREATE TABLE participant_unit (
    participant_id INT,
    unit_id INT,
    PRIMARY KEY (participant_id, unit_id),
    FOREIGN KEY (participant_id) REFERENCES participant(participant_id),
    FOREIGN KEY (unit_id) REFERENCES unit(unit_id)
);
