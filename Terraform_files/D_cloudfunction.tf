# Get_chall_function
# If deploying each time API_KEY resets, then need to make sure I delete the function first and remake it. Which is annoying
resource "google_cloudfunctions2_function" "get_chall_euw_function" {
  name = "get-chall-euw-function10"
  location = "europe-west2"
  description = "Get challengers leaderboard function"

  build_config {
    runtime = "python39"
    entry_point = "get_chall_ladder_data"  # Set the entry point 
    source {
      storage_source {
        bucket = var.python_script_bucket_name
        object = "Get_challengers.zip"
      }
    }
  }

  service_config {
    max_instance_count  = 1
    available_memory    = "256M"
    timeout_seconds     = 60
  }
} 

resource "google_project_iam_member" "gcf-invoking" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "user:Ceesjdu@gmail.com"#${google_service_account.account.email}"
}
resource "google_project_iam_member" "gcf-invoking-email-service-accout" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:json-test-377211@appspot.gserviceaccount.com"#${google_service_account.account.email}"
}



resource "google_cloudfunctions2_function" "get_puuid_euw_function" {
  name = "get-puuid-euw-function10"
  location = "europe-west2"
  description = "Get puuid from reading chall csv for euw function"

  build_config {
    runtime = "python39"
    entry_point = "process_csv_file"  # Set the entry point 
    source {
      storage_source {
        bucket = var.python_script_bucket_name
        object = "Get_puuid.zip"
      }
    }
  }

  service_config {
    max_instance_count  = 1
    available_memory    = "256M"
    timeout_seconds     = 60
  }
} 

# # terraform the composer environment too 