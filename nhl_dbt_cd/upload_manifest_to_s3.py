import boto3
import argparse
import os


#Instantiate s3 client 
s3 = boto3.resource('s3')

parser = argparse.ArgumentParser(description='A parser for dbt_CI_CD manifest upload.')
parser.add_argument("--path")

def load_dbt_manifest_to_s3(path_to_manifest):
    '''
    Loads dbt manifest in specified location to bucket in s3.

    '''
    s3.meta.client.upload_file(
        path_to_manifest, 
        os.environ['AWS_S3_BUCKET'], 
        'manifest.json')


args = parser.parse_args()

path = args.path

load_dbt_manifest_to_s3(path)