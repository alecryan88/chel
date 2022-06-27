from dagster_dbt.asset_defs import load_assets_from_dbt_project

dbt_assets = load_assets_from_dbt_project(
    project_dir = os.environ['DBT_DIR'], 
    profiles_dir = os.environ['DBT_DIR']
    )

asset(
    required_resource_keys={'s3'},
    compute_kind='python',
    group_name = 'nhl_game_data_s3'
)
def download_prod_manifest(context, dbt_assets):
    '''
    Load game_data to s3 in JSON format.
    '''

    for game_id in extract_game_ids_to_list:
        r = requests.get(f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/feed/live')
    
        #Store JSON respose
        json = io.BytesIO(r.content)

        context.resources.s3.put_object(
            Body=json,
            Bucket='nhl-analytics',
            Key=f'nhl-game-data/partition_date={partition_key}/{game_id}.json'
        )

import boto3
import os
 
s3_client = boto3.client('s3')

filename = 'manifest.json'
location = 'nhl_dbt/ci_manifest/manifest.json'

bucket = 'nhl-prod-dbt-manifest'

print(f"Loading file to {location}.")

s3_client.download_file(
    Bucket=bucket, 
    Key=filename, 
    Filename=location
    )

print(f"Successly loaded file to {location}.")


        