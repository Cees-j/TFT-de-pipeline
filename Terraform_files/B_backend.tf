terraform {
backend "gcs" {
  credentials = "credentials.json"
  bucket = "terraform-state-10001-json-test"   # GCS bucket name to store terraform tfstate
  prefix = "terraform/state"           # Update to desired prefix name. Prefix name should be unique for each Terraform project having same remote state bucket.
 
  depends_on = [google_storage_bucket.terraform_state_bucket]
  }
}