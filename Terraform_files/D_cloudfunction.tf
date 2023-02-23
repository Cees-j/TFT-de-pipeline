# Get_chall_function
# If deploying each time API_KEY resets, then need to make sure I delete the function first and remake it. Which is annoying
resource "google_cloudfunctions2_function" "get_chall_euw_function2" {
  name = "get-chall-euw-function40"
  location = "europe-west2"
  description = "Get challengers leaderboard function"

  build_config {
    runtime = "python39"
    entry_point = "entrypoint"  # Set the entry point 
    source {
      storage_source {
        bucket = var.python_script_bucket_name
        object = "Get_challengers2.zip"
      }
    }
  }

  service_config {
    max_instance_count  = 1
    available_memory    = "256M"
    timeout_seconds     = 60
  
  
    secret_environment_variables {
      key        = var.api_secret_id
      project_id = var.project_id
      secret     = var.api_secret_id
      version    = "latest"
    }
  }
  depends_on = [google_secret_manager_secret_iam_member.api_key_secret_iam_02]
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



resource "google_cloudfunctions2_function" "get_puuid_euw_function2" {
  name = "get-puuid-euw-function40"
  location = "europe-west2"
  description = "Get puuid from reading chall csv for euw function"

  build_config {
    runtime = "python39"
    entry_point = "entrypoint"  # Set the entry point 
    source {
      storage_source {
        bucket = var.python_script_bucket_name
        object = "Get_puuid2.zip"
      }
    }
  }

  service_config {
    max_instance_count  = 1
    available_memory    = "256M"
    timeout_seconds     = 60

  secret_environment_variables {
    key        = var.api_secret_id
    project_id = var.project_id
    secret     = var.api_secret_id
    version    = "latest"
    }
  }
  depends_on = [google_storage_bucket_object.get_puuid_script2]
} 


resource "google_cloudfunctions2_function" "get_matches_euw_function2" {
  name = "get-matches-euw-function40"
  location = "europe-west2"
  description = "Get puuid from reading chall csv for euw function"

  build_config {
    runtime = "python39"
    entry_point = "entrypoint"  # Set the entry point 
    source {
      storage_source {
        bucket = var.python_script_bucket_name
        object = "Get_matches2.zip"
      }
    }
  }

  service_config {
    max_instance_count  = 1
    available_memory    = "256M"
    timeout_seconds     = 60

  secret_environment_variables {
    key        = var.api_secret_id
    project_id = var.project_id
    secret     = var.api_secret_id
    version    = "latest"
    }
  }
  depends_on = [google_storage_bucket_object.get_matches_script]
} 


resource "google_cloudfunctions2_function" "get_detailed_matches_euw_function2" {
  name = "get-detailed-matches-euw-function41"
  location = "europe-west2"
  description = "Get puuid from reading chall csv for euw function"

  build_config {
    runtime = "python39"
    entry_point = "entrypoint"  # Set the entry point 
    source {
      storage_source {
        bucket = var.python_script_bucket_name
        object = "Get_detailed_matches2.zip"
      }
    }
  }

  service_config {
    max_instance_count  = 1
    available_memory    = "256M"
    timeout_seconds     = 60

  secret_environment_variables {
    key        = var.api_secret_id
    project_id = var.project_id
    secret     = var.api_secret_id
    version    = "latest"
    }
  }
  depends_on = [google_storage_bucket_object.get_detailed_matches_script]
} 
# # terraform the composer environment too 