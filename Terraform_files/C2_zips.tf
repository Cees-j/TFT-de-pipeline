data "archive_file" "zip_get_chall_script_euw" {
  type        = "zip"
  source_dir = "../Python_scripts/Get_challengers_euw"
  output_path = "../Python_scripts/Get_challengers_euw/Get_challengers.zip"
}

resource "google_storage_bucket_object" "get_chall_script" {
  name   = "Get_challengers.zip"
  bucket = var.python_script_bucket_name
  source = "../Python_scripts/Get_challengers_euw/Get_challengers.zip"

  # Set the content type of the object
  content_type = "application/zip"
}
