# Specify the GCP Provider
provider "google" {
credentials = file("credentials.json")
project = var.project_id
region  = var.region
}

# Create a GCS Bucket
resource "google_storage_bucket" "python_script_code_bucket" {
name     = var.bucket_name
location = var.region
}