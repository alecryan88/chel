from dagster import AssetKey, asset_sensor, RunRequest, get_dagster_logger, PartitionSetDefinition
from datetime import datetime

def create_snowflake_asset_sensor(key, snowflake_job):

    @asset_sensor(
        asset_key=AssetKey(key),
        job=snowflake_job
    )
    def snowflake_sensor(context, asset_event):
        asset_partition = asset_event.dagster_event.partition
        yield RunRequest(
            run_key=context.cursor,
            run_config={
                "resources": {
                    "snowflake": {
                        "config": {
                            'account': 'pua88554',
                            'user':'flyers88', 
                            'password':'VampireWeekend2021',
                            'database': 'NHL_DB',
                            'warehouse': 'NHL_ANALYTICS'
                            }
                        },
                    "run_parameters" : {
                        "config": {
                            "run_date" : asset_partition
                            }
                        }
                    }
                }
            )

    return snowflake_sensor