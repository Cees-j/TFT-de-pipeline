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
  
  # Need to change this secret_data a lot # hopefully just changes the internals, then dont need to remake functions etc
  # Ok so can just change this secret data, and then as functions are using 'latest' version of secret it will
  # use last input api key as reference.
  # Put this as a tf.vars
  secret_data = "RGAPI-8b11abca-8522-49c9-b1e0-0d91d0a551c6"

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

