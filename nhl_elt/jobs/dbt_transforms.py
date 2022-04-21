import pandas as pd
from dagster import AssetGroup
from dagster_dbt import dbt_cli_resource
from dagster_dbt.asset_defs import load_assets_from_dbt_project

dbt_configured_resource = dbt_cli_resource.configured(
    {"profiles-dir": 'dbt', "project-dir": 'dbt'}
)

assets = load_assets_from_dbt_project(project_dir = 'dbt', profiles_dir = 'dbt')

dbt_asset_group = AssetGroup(assets,
resource_defs={
        'dbt': dbt_configured_resource
    }
)

dbt_transforms = dbt_asset_group.build_job(name="dbt_transforms")