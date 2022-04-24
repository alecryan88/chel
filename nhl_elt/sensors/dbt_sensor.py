from dagster import AssetKey, asset_sensor, RunRequest, get_dagster_logger
from datetime import datetime


def create_dbt_asset_sensor(key, dbt_run):

    @asset_sensor(
        asset_key=AssetKey(key),
        job=dbt_run
    )
    def dbt_sensor(context, asset_event):
        asset_partition = asset_event.dagster_event.partition

        yield RunRequest(
            run_key=context.cursor,
            run_config={
                "resources": {
                    "dbt": {
                        "config": {
                            "profiles_dir" : "dbt",
                            "project_dir" : "dbt",
                            "var" : { 'run_date' : asset_partition}
                        }
                    }
                }
            }
        )

    return dbt_sensor