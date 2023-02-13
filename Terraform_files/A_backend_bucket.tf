# Specify the GCP Provider
provider "google" {
credentials = file("credentials.json")
project = var.project_id
region  = var.region
}

resource "google_storage_bucket" "terraform_state_bucket" {
  name          = var.terraform_state_bucket_name
  location      = var.region
  force_destroy = true
}

