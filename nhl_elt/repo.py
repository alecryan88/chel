from dagster import repository, build_schedule_from_partitioned_job
from nhl_elt.jobs.stage_data_in_s3 import * 
from nhl_elt.jobs.load_data_to_snowflake import * 
from nhl_elt.jobs.dbt_transforms import *
from nhl_elt.sensors.dbt_sensor import *

@repository
def nhl_elt_prod():
    return [
        build_schedule_from_partitioned_job(
            stage_game_data,
            description = 'Downloads NHL API data and stages in s3.',
            hour_of_day = 2,

        ),
        build_schedule_from_partitioned_job(
            load_data_to_snowflake,
            description = 'Copies data from s3 to Snowflake after new s3 data is detected',
            hour_of_day = 3 
        ),
        create_dbt_sensor('copy_partition_into_snowflake',dbt_transforms)
    ]