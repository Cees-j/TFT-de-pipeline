from google.cloud import bigquery
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
# Initialize the BigQuery client and get a reference to the destination table
client = bigquery.Client()
table_ref = client.dataset('get_chall_euw_dataset_id').table('Detailed-data-dump-euw')

# Set the source URI using a wildcard for the filename
uri = 'gs://csv-store-10001/sailmate3*'

# Configure the job options
job_config = bigquery.LoadJobConfig(
    autodetect=True,
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1
)

# Load the data into the table
load_job = client.load_table_from_uri(
    uri,
    table_ref,
    job_config=job_config
)
load_job.result()
