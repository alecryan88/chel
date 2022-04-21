from dagster import AssetKey, asset_sensor

def create_dbt_sensor(key, job):
    @asset_sensor(
        asset_key=AssetKey(key),
        job=job
    )
    def dbt_sensor(context, asset_event):
        yield RunRequest(
            run_key=context.cursor,
            run_config={
                "ops": {
                    "read_materialization": {
                        "config": {
                            "asset_key": asset_event.dagster_event.asset_key.path,
                            "run_date" : context.output_asset_partition_key()
                        }
                    }
                }
            },
        )

    return dbt_sensor