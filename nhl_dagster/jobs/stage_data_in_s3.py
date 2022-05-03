from dagster import AssetGroup
from dagster_aws.s3.resources import s3_resource
from nhl_dagster.assets.nhl_to_s3 import *


s3_resource_configured = s3_resource.configured(
    {'profile_name':'dagster_dev'}
)

assets = [
    extract_game_ids_to_list, 
    load_game_data_to_s3
    ]

asset_group = AssetGroup(assets, 
    resource_defs={
        's3': s3_resource_configured,
    }
)

stage_game_data = asset_group.build_job(name="stage_game_data")