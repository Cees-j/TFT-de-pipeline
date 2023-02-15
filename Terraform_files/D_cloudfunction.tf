# Get_chall_function
# If deploying each time API_KEY resets, then need to make sure I delete the function first and remake it. Which is annoying
resource "google_cloudfunctions2_function" "get_chall_euw_function" {
  name = "get-chall-euw-function6"
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

  event_trigger {
    allow_unauthenticated = true
  }
} 
