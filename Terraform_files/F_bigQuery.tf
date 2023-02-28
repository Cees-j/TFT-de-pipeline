## IF SETUP
# This terraform file is to be ran after a csv has been retrieved and stored in google cloud storage CSV store
##
resource "google_bigquery_dataset" "euw-dataset" {
  dataset_id                  = var.get_chall_euw_dataset_id
  project                     = var.project_id
  friendly_name               = "euw-dataset"
  description                 = "Stores detailed match data for euw players"
  location                    = "europe-west2"   # # # # # # # # CRUCIAL
  default_table_expiration_ms = 18000000

  labels = {
    env = "default"
  }
}


resource "google_bigquery_table" "my_detailed_matches_table" {
  dataset_id = var.get_chall_euw_dataset_id
  table_id   = "Detailed-data-dump-euw"
  
  # Set the schema to null to enable auto-detection
  schema = null

  # Set the source format and path for the data in Cloud Storage
  # Makes a table of all the data from detailed match data and inputs into a table
  # Would need to be deployed after the data is retrieved.
  external_data_configuration {
    source_format = "CSV"
    source_uris    = [var.detailed_match_data_url]
    autodetect     = true
  }

  depends_on = [google_bigquery_dataset.euw-dataset]
}