import boto3
import os
 
s3_client = boto3.client('s3', 
                      aws_access_key_id='AKIAZNPFTOMRZY4URRGB',
                      aws_secret_access_key='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',
                      region_name='us-east-1'
                      )

filename = 'manifest.json'
location = 'nhl_dbt/ci_manifest/manifest.json'

bucket = 'nhl-prod-dbt-manifest'

s3_client.download_file(
    Bucket=bucket, 
    Key=filename, 
    Filename=location
    )

print("Success.")