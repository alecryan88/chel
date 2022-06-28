from dagster_dbt.asset_defs import load_assets_from_dbt_project
from dagster import asset
import boto3
import os

dbt_dir = os.environ['DBT_DIR']

dbt_assets = load_assets_from_dbt_project(
    project_dir = dbt_dir, 
    profiles_dir = dbt_dir
    )

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


@asset(
    required_resource_keys={'s3', 'dbt'},
    compute_kind='python',

)
def download_dbt_artifacts(context, game_finals):
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