from dagster import AssetGroup, DailyPartitionsDefinition, load_assets_from_package_module
from nhl_dagster.resources.resources import * 
from nhl_dagster.assets.nhl_to_s3 import *
from nhl_dagster.assets.s3_to_snowflake import *
from nhl_dagster.assets.dbt_assets import *

assets = [
    extract_game_ids_to_list,
    load_game_data_to_s3,
    RAW_NHL_GAME_DATA,
    *dbt_assets,
    upload_dbt_artifacts
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