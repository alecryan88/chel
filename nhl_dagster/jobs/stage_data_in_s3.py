from dagster import AssetGroup
from dagster_aws.s3.resources import s3_resource
from nhl_dagster.assets.nhl_to_s3 import *
import os

assets = [
    extract_game_ids_to_list, 
    load_game_data_to_s3
    ]

asset_group = AssetGroup(assets, 
    resource_defs={
        's3': s3_resource
    }
)

stage_game_data = asset_group.build_job(name="stage_game_data")