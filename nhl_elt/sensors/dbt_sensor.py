from dagster import AssetKey, asset_sensor, RunRequest, get_dagster_logger
from datetime import datetime


def create_dbt_asset_sensor(key, dbt_run):

    @asset_sensor(
        asset_key=AssetKey(key),
        job=dbt_run
    )
    def dbt_sensor(context, asset_event):
        
        upstream_run = context.instance.get_run_by_id(asset_event.run_id)

        #Get the run config of the upstream asset_event
        upstream_run_config = upstream_run.run_config

        #Parse out the run dat from the upstream asset_event run_config
        run_date = upstream_run_config['resources']['run_parameters']['config']['run_date']

        yield RunRequest(
            run_key=context.cursor,
            run_config={
                "resources": {
                    "dbt": {
                        "config": {
                            "profiles_dir" : "dbt",
                            "project_dir" : "dbt",
                            "var" : { 'run_date' : run_date}
                        }
                    }
                }
            }
        )

    return dbt_sensor