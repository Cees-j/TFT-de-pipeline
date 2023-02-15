# Data Engineering Project
This is a data engineering project that retrieves data from an API, transforms it, and loads it into BigQuery using a set of Python scripts. The project is designed to use Cloud Functions for retrieving and transforming data, and to run in GCP Cloud Composer, an Apache Airflow-based workflow orchestration service. The infrastructure for the project is provisioned using Terraform.

# Project Structure
The project consists of the following files and directories:

Python_scripts/: Directory containing the Python scripts for retrieving and transforming data.
dags/: Directory containing the Airflow DAG definition file for scheduling the Python scripts to run.
requirements.txt: File containing the Python package dependencies for the project.
Terraform_files/: Directory containing the Terraform configuration files for provisioning the cloud infrastructure.

# Setup
To set up the project, follow these steps:

TBC 

# Dependencies
The project relies on the following Python packages, which are specified in the requirements.txt file:

google-cloud-bigquery
requests
pandas
google-cloud-storage
google-auth
google-cloud-bigquery