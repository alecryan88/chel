from dagster import AssetGroup, DailyPartitionsDefinition
from nhl_dagster.resources.resources import * 
from nhl_dagster.assets.nhl_to_s3 import *
from nhl_dagster.assets.s3_to_snowflake import *
from dagster_dbt.asset_defs import load_assets_from_dbt_project
import os

dbt_dir = os.environ['DBT_DIR']

dbt_assets = load_assets_from_dbt_project(project_dir=dbt_dir, profiles_dir=dbt_dir)

assets = [
    extract_game_ids_to_list,
    load_game_data_to_s3,
    delete_partition_from_snowflake,
    copy_partition_into_snowflake,
    *dbt_assets
]

asset_group = AssetGroup(
    assets, 
    resource_defs={
        's3': s3_resource,
        'snowflake': snowflake_resource_configured,
        'dbt': dbt_resource_configured   
    }
)

nhl_game_data = asset_group.build_job(name="nhl_game_data")