from dagster import repository, build_schedule_from_partitioned_job
from nhl_elt.jobs.stage_data_in_s3 import stage_game_data
from nhl_elt.jobs.load_data_to_snowflake import load_data_to_snowflake
from nhl_elt.jobs.dbt_transforms import dbt_transforms
from nhl_elt.sensors.dbt_sensor import create_dbt_asset_sensor
from nhl_elt.sensors.snowflake_sensor import create_snowflake_asset_sensor


@repository
def nhl_elt_prod():
    return [
        build_schedule_from_partitioned_job(
            stage_game_data,
            description = 'Downloads NHL API data and stages in s3.',
            hour_of_day = 4,
            minute_of_hour = 56

        ),
        
        create_snowflake_asset_sensor(
            'load_game_data_to_s3', load_data_to_snowflake
        ),

        create_dbt_asset_sensor(
            'copy_partition_into_snowflake', dbt_transforms
        )

    ]