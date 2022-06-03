import boto3
import os
 
s3_client = boto3.client('s3')

filename = 'manifest.json'
location = 'nhl_dbt/ci_manifest/manifest.json'

bucket = 'nhl-prod-dbt-manifest'

s3_client.download_file(bucket, filename, location)

print("Success.")