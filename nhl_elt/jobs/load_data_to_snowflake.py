from dagster import AssetGroup
from dagster_snowflake import snowflake_resource
from nhl_elt.assets.s3_to_snowflake import *
import json

snowflake_resource_configured = snowflake_resource.configured(
    {
        'account': 'pua88554',
        'user':'flyers88', 
        'password':'VampireWeekend2021',
        'database': 'NHL_DB',
        'warehouse': 'NHL_ANALYTICS'
    }
)

assets = [
    delete_partition_from_snowflake, 
    copy_partition_into_snowflake
    ]

asset_group = AssetGroup(assets, 
    resource_defs={
        'snowflake': snowflake_resource_configured,
    }
)

load_data_to_snowflake = asset_group.build_job(name="load_data_to_snowflake")