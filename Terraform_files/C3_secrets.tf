resource "google_secret_manager_secret" "secret-basic_api_key" {
  secret_id = var.api_secret_id

  labels = {
    label = "defining_an_api_key"
  }

  replication {
    user_managed {
      replicas {
        location = "europe-west2"
      }
      replicas {
        location = "us-east1"
      }
    }
  }
}

resource "google_secret_manager_secret_version" "example_secret_version_api_key" {
  secret    = google_secret_manager_secret.secret-basic_api_key.id 
  

  secret_data = var.actual_api_key # this var needs to be changed to update api_key to allow functions

  depends_on = [google_secret_manager_secret.secret-basic_api_key]
    
  
}

# Setting api_key secret permissions so function can be made later
resource "google_secret_manager_secret_iam_member" "api_key_secret_iam_02" {
  secret_id   = "API_KEY" # What secret is named
  project    =  var.project_id
  role       = "roles/secretmanager.secretAccessor"

  # Can set member as a variable
  member     = "serviceAccount:79899012534-compute@developer.gserviceaccount.com" # This is Default

  
  depends_on = [google_secret_manager_secret.secret-basic_api_key]
}

