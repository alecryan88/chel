import boto3
import argparse
import os
import json

#Instantiate s3 client 
s3 = boto3.client('s3')

#Name of file in S3
file_name = 'manifest.json'

#Where the file will be downloaded to
object_name = 'nhl_dbt/ci_manifest/manifest.json'

with open(path) as file:
    manifest = json.load(file)

    s3.put_object(
    Body=json.dumps(manifest),
    Bucket=os.environ['AWS_S3_BUCKET'],
    Key='manifest.json'
    )