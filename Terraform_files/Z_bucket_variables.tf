variable "project_id" {
description = "Google Project ID."
type        = string
}


variable "python_script_bucket_name" {
description = "GCS Bucket name. Value should be unique ."
type        = string
}

variable "csv_store_bucket_name" {
description = "GCS Bucket name. Value should be unique ."
type        = string
}

variable "terraform_state_bucket_name" {
description = "GCS Bucket name. Value should be unique ."
type        = string
}

variable "region" {
description = "Google Cloud region"
type        = string
default     = "europe-west2"
}

variable "get_chall_euw_url" {
    description = "gs url for bucket and file"
    type        = string
    default     = "europe-west2"
}

variable "detailed_match_data_url" {
    description = "gs url for bucket and file, detailed matches"
    type        = string
    default     = "europe-west2"
}

variable "get_chall_euw_dataset_id" {
    description = "id for get_chall dataset"
    type        = string
    default     = "europe-west2"
}

variable "api_secret_id" {
    description = "api_key stored in secrets manager"
    type        = string
    default     = "https://developer.riotgames.com/"
}