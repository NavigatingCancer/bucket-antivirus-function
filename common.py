# -*- coding: utf-8 -*-
# Upside Travel, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import errno
import datetime
import os
import os.path

import boto3

AV_DEFINITION_S3_BUCKET = os.getenv("AV_DEFINITION_S3_BUCKET")
AV_DEFINITION_S3_PREFIX = os.getenv("AV_DEFINITION_S3_PREFIX", "clamav_defs")
AV_DEFINITION_PATH = os.getenv("AV_DEFINITION_PATH", "/tmp/clamav_defs")
AV_SCAN_BUCKET_NAME = os.getenv("AV_SCAN_BUCKET_NAME", None)
AV_SCAN_START_SNS_ARN = os.getenv("AV_SCAN_START_SNS_ARN")
AV_SCAN_START_METADATA = os.getenv("AV_SCAN_START_METADATA", "av-scan-start")
AV_SIGNATURE_METADATA = os.getenv("AV_SIGNATURE_METADATA", "av-signature")
AV_SIGNATURE_OK = "OK"
AV_SIGNATURE_UNKNOWN = "UNKNOWN"
AV_STATUS_CLEAN = os.getenv("AV_STATUS_CLEAN", "not_malicious")
AV_STATUS_INFECTED = os.getenv("AV_STATUS_INFECTED", "malicious")
AV_STATUS_METADATA = os.getenv("AV_STATUS_METADATA", "fss-scan-result")
AV_STATUS_SNS_ARN = os.getenv("AV_STATUS_SNS_ARN")
AV_STATUS_SNS_PUBLISH_CLEAN = os.getenv("AV_STATUS_SNS_PUBLISH_CLEAN", "True")
AV_STATUS_SNS_PUBLISH_INFECTED = os.getenv("AV_STATUS_SNS_PUBLISH_INFECTED", "True")
AV_TIMESTAMP_METADATA = os.getenv("AV_TIMESTAMP_METADATA", "av-timestamp")
CLAMAVLIB_PATH = os.getenv("CLAMAVLIB_PATH", "./bin")
CLAMSCAN_PATH = os.getenv("CLAMSCAN_PATH", "./bin/clamscan")
FRESHCLAM_PATH = os.getenv("FRESHCLAM_PATH", "./bin/freshclam")

AV_DEFINITION_FILE_PREFIXES = ["main", "daily", "bytecode"]
AV_DEFINITION_FILE_SUFFIXES = ["cld", "cvd"]
SNS_ENDPOINT = os.getenv("SNS_ENDPOINT", None)
S3_ENDPOINT = os.getenv("S3_ENDPOINT", None)
LAMBDA_ENDPOINT = os.getenv("LAMBDA_ENDPOINT", None)
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", None)


def create_dir(path):
    if not os.path.exists(path):
        try:
            print("Attempting to create directory %s.\n" % path)
            os.makedirs(path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


def get_timestamp():
    return datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S UTC")


def get_s3_objects_from_key_names(key_names, bucket_name):
    s3 = boto3.resource("s3", endpoint_url=S3_ENDPOINT)
    all_objects = []
    # translates key names into s3 objects and puts them in an array
    timestamp = get_timestamp()
    print("Getting S3 Objects from key names starting at %s\n" % timestamp)
    for key in key_names:
        key_string = str(key)
        object = s3.Object(bucket_name, key_string)
        all_objects.append(object)
    # returns array of s3 objects
    timestamp = get_timestamp()
    print("Getting S3 Objects from key names finished at %s\n" % timestamp)
    return all_objects
