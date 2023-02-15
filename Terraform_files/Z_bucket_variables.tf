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