import boto3
import os
 
s3_client = boto3.client('s3')

#Name of file in S3
file_name = 'manifest.json'

#Where the file will be downloaded to
object_name = 'nhl_dbt/ci_manifest/manifest.json'

#Bucket where the file exists
bucket = 'dbt-docs-chel'

print(f"Loading file to {object_name}.")

s3_client.download_file(
    Bucket=bucket, 
    Key=file_name, 
    Filename=object_name
    )

print(f"Successly loaded file to {object_name}.")