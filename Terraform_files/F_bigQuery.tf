## IF SETUP
# This terraform file is to be ran after a csv has been retrieved and stored in google cloud storage CSV store
##
resource "google_bigquery_dataset" "euw-dataset" {
  dataset_id                  = var.get_chall_euw_dataset_id
  project                     = var.project_id
  friendly_name               = "euw-dataset"
  description                 = "Stores data for euw players"
  location                    = "EU"
  default_table_expiration_ms = 3600000

  labels = {
    env = "default"
  }
}

# Have to run this twice, once for dataset, once for table

resource "google_bigquery_table" "my_table" {
  dataset_id = var.get_chall_euw_dataset_id
  table_id   = "Chall-data-euw"
  
  # Set the schema to null to enable auto-detection
  schema = null

  # Set the source format and path for the data in Cloud Storage
  # Will take the challenger csv url when uploaded, so is dependent on being named correctly
  external_data_configuration {
    source_format = "CSV"
    source_uris    = [var.get_chall_euw_url]
    autodetect     = true
  }
}