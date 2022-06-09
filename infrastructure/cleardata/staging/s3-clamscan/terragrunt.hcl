terraform {
  source = "../../../modules//s3-clamscan"
}

include {
  path = find_in_parent_folders()
}

inputs = {
  lambda_version  = "v3.0.0"
  lambda_package  = "antivirus"
  av_scan_buckets = ["nc-staging"]
}
