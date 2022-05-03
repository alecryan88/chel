from dagster import AssetGroup
from dagster_dbt import dbt_cli_resource
from dagster_dbt.asset_defs import load_assets_from_dbt_project

DBT_DIR = '/opt/dagster/app/nhl_dbt'

dbt_assets = load_assets_from_dbt_project(project_dir = DBT_DIR, profiles_dir = DBT_DIR)

dbt_asset_group = AssetGroup(
    dbt_assets,
    resource_defs={
            'dbt': dbt_cli_resource
        }
)

dbt_transforms = dbt_asset_group.build_job(name="dbt_transforms")