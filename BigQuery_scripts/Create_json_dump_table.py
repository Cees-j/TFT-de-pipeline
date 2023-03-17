from google.cloud import bigquery
import os
'''Makes the initial json dump from all files saved as sailmate3*'''


def load_csv_to_bigquery(dataset_id: str, table_id: str, uri: str) -> None:
    '''
    Loads CSV files from Google Cloud Storage into a BigQuery table.
    Makes the initial json dump from all files saved as sailmate3*
    
    
    dataset_id (str): ID of the BigQuery dataset to load the data into.
    table_id (str): ID of the BigQuery table to load the data into.
    uri (str): URI of the CSV file(s) to load into BigQuery.
    '''
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
    client = bigquery.Client()
    table_ref = client.dataset(dataset_id).table(table_id)

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1
    )

    load_job = client.load_table_from_uri(
        uri,
        table_ref,
        job_config=job_config
    )

    load_job.result()
