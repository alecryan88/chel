from dagster_dbt.asset_defs import load_assets_from_dbt_project

dbt_assets = load_assets_from_dbt_project(
    project_dir = os.environ['DBT_DIR'], 
    profiles_dir = os.environ['DBT_DIR']
    )