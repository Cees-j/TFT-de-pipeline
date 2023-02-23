# data "archive_file" "zip_get_chall_script_euw" {
#   type        = "zip"
#   source_dir = "../Python_scripts/Get_challengers_euw"
#   output_path = "../Python_scripts/Get_challengers_euw/Get_challengers.zip"
# }

# resource "google_storage_bucket_object" "get_chall_script" {
#   name   = "Get_challengers.zip"
#   bucket = var.python_script_bucket_name
#   source = "../Python_scripts/Get_challengers_euw/Get_challengers.zip"

#   # Set the content type of the object
#   content_type = "application/zip"
# }


data "archive_file" "zip_get_puuid_script_euw2" {
  type        = "zip"
  source_dir = "../Python_scripts/Get_puuid_euw2"
  output_path = "../Python_scripts/Get_puuid_euw2/Get_puuid.zip"
}

resource "google_storage_bucket_object" "get_puuid_script2" {
  name   = "Get_puuid2.zip"
  bucket = var.python_script_bucket_name
  source = "../Python_scripts/Get_puuid_euw2/Get_puuid.zip"

  # Set the content type of the object
  content_type = "application/zip"
}

data "archive_file" "zip_get_chall_script_euw2" {
  type        = "zip"
  source_dir = "../Python_scripts/Get_challengers_euw2"
  output_path = "../Python_scripts/Get_challengers_euw2/Get_challengers.zip"
}

resource "google_storage_bucket_object" "get_chall_script" {
  name   = "Get_challengers2.zip"
  bucket = var.python_script_bucket_name
  source = "../Python_scripts/Get_challengers_euw2/Get_challengers.zip"

  # Set the content type of the object
  content_type = "application/zip"
}

data "archive_file" "zip_get_matches_script_euw2" {
  type        = "zip"
  source_dir = "../Python_scripts/Get_matches_euw2"
  output_path = "../Python_scripts/Get_matches_euw2/Get_matches.zip"
}

resource "google_storage_bucket_object" "get_matches_script" {
  name   = "Get_matches2.zip"
  bucket = var.python_script_bucket_name
  source = "../Python_scripts/Get_matches_euw2/Get_matches.zip"

  # Set the content type of the object
  content_type = "application/zip"
}

data "archive_file" "zip_get_detailed_matches_script_euw2" {
  type        = "zip"
  source_dir = "../Python_scripts/Get_detailed_matches_euw2"
  output_path = "../Python_scripts/Get_detailed_matches_euw2/Get_detailed_matches.zip"
}

resource "google_storage_bucket_object" "get_detailed_matches_script" {
  name   = "Get_detailed_matches2.zip"
  bucket = var.python_script_bucket_name
  source = "../Python_scripts/Get_detailed_matches_euw2/Get_detailed_matches.zip"

  # Set the content type of the object
  content_type = "application/zip"
}

