# Create a GCS Bucket
resource "google_storage_bucket" "python_script_code_bucket" {
name     = var.python_script_bucket_name
location = var.region
force_destroy = true

#depends_on = [google_storage_bucket.terraform_state_bucket]
}

resource "google_storage_bucket" "csv_store" {
name = var.csv_store_bucket_name
location = var.region  
force_destroy = true

depends_on = [google_storage_bucket.python_script_code_bucket]
}

