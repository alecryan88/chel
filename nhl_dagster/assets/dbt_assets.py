from dagster_dbt.asset_defs import load_assets_from_dbt_project
from dagster import asset
import boto3
import os

dbt_dir = os.environ['DBT_DIR']

dbt_assets = load_assets_from_dbt_project(
    project_dir = dbt_dir, 
    profiles_dir = dbt_dir
    )


def upload_file_using_client():
    """
    Uploads file to S3 bucket using S3 client object
    :return: None
    """
    s3 = boto3.client("s3")
    bucket_name = "binary-guy-frompython-1"
    object_name = "sample1.txt"
    file_name = os.path.join(pathlib.Path(__file__).parent.resolve(), "sample_file.txt")
    response = s3.upload_file(file_name, bucket_name, object_name)
    pprint(response)  # prints Non

@asset(
    required_resource_keys={'s3', 'dbt'},
    compute_kind='python',

)
def upload_dbt_artifacts(context, game_finals):
    '''
    Load artifacts to s3.
    '''

    bucket_name = "dbt-docs-chel"
    
    #dbt Artifacts
    catalog = f"{dbt_dir}/target/catalog.json"
    index = f"{dbt_dir}/target/index.html"
    manifest = f"{dbt_dir}/target/manifest.json"

    dbt_artifacts = [catalog, manifest, index]

    for i in dbt_artifacts:
        object_name = i.replace(f"{dbt_dir}/target/","")
        context.resources.s3.upload_file(i, bucket_name, object_name)