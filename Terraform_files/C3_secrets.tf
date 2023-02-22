resource "google_secret_manager_secret" "secret-basic_api_key" {
  secret_id = var.api_secret_id # Can set this as a variable

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
  secret    = google_secret_manager_secret.secret-basic_api_key.id # uses the return attrib ref from above
  
  # Set the value of the new version
  secret_data = "RGAPI-55f09d30-553e-470a-88de-cc98f2db78ba"

  depends_on = [google_secret_manager_secret.secret-basic_api_key]
    
  
}

# Setting api_key secret permissions so function can be made later
resource "google_secret_manager_secret_iam_member" "api_key_secret_iam_02" {
  secret_id   = var.api_secret_id # What secret is named
  project    =  var.project_id
  role       = "roles/secretmanager.secretAccessor"
  # Can set member as a variable
  member     = "serviceAccount:79899012534-compute@developer.gserviceaccount.com" # This is Default
  # computer service account. 
  depends_on = [google_secret_manager_secret.secret-basic_api_key]
}

