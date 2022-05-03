from dagster import AssetGroup, make_values_resource
from dagster_snowflake import snowflake_resource
from nhl_dagster.assets.s3_to_snowflake import *
import json

assets = [
    delete_partition_from_snowflake, 
    copy_partition_into_snowflake
    ]

asset_group = AssetGroup(assets, 
    resource_defs={
        'snowflake': snowflake_resource,
        'run_parameters': make_values_resource()
        }
)

load_data_to_snowflake = asset_group.build_job(name="load_data_to_snowflake")