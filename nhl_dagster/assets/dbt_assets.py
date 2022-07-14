from dagster_dbt.asset_defs import load_assets_from_dbt_project
from nhl_dagster.partitions.partitions import daily_partitions_def
from dagster import asset, AssetIn
import os, subprocess, boto3

dbt_dir = os.environ['DBT_DIR']

dbt_assets = load_assets_from_dbt_project(
    project_dir = dbt_dir, 
    profiles_dir = dbt_dir
    )

@asset(
    required_resource_keys={'s3', 'dbt'},
    compute_kind='python'
)
def generate_dbt_artifacts(context, game_finals):
    '''
    dbt generate command for refresh of dbt artifacts:
    - index.html
    - manifest.json
    - catalog.json
    '''

    os.chdir(dbt_dir)
    
    docs_generate_cmd = "dbt docs generate --profiles-dir . --target prod --no-compile"

    subprocess.run(docs_generate_cmd, shell =True) 


@asset(
    required_resource_keys={'s3', 'dbt'},
    compute_kind='python'
)
def upload_dbt_artifacts(context, generate_dbt_artifacts):
    '''
    Load artifacts to s3.
    '''
    
    bucket_name = os.environ['DBT_DOCS_BUCKET']
    
    #dbt Artifacts
    catalog = f"{dbt_dir}/target/catalog.json"
    index = f"{dbt_dir}/target/index.html"
    manifest = f"{dbt_dir}/target/manifest.json"

    dbt_artifacts = [catalog, manifest, index]

    for i in dbt_artifacts:

        if i.split(".")[-1] == 'json':
            content_type = 'application/json'
        else: 
            content_type = 'text/html'

        key = i.replace(f"{dbt_dir}/target/","")
        context.resources.s3.put_object(
            Body=open(i, 'rb'),
            Bucket=bucket_name,
            Key=key.strip(),
            ContentType=content_type
        )