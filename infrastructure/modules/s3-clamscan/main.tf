# The AWS partition (commercial or govcloud)
data "aws_partition" "current" {}

data "terraform_remote_state" "kms_master_key" {
  backend = "s3"
  config = {
    region  = var.terraform_state_aws_region
    bucket  = var.terraform_state_s3_bucket
    key     = "${var.terraform_state_aws_profile}/${var.env_name}/kms-master-key/terraform.tfstate"
    encrypt = true
    profile = var.terraform_state_aws_profile
  }
}

locals {
  lambda_package_key = var.lambda_package_key != null ? var.lambda_package_key : "${var.lambda_package}/${var.lambda_version}/${var.lambda_package}.zip"
}
