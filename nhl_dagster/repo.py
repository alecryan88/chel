from dagster import repository, build_schedule_from_partitioned_job
from nhl_dagster.jobs.nhl_jobs import run_elt


@repository
def nhl_elt():
    return [
        build_schedule_from_partitioned_job(
            run_elt,
            description = 'Downloads NHL API data to s3, copies from snowflake and builds dbt models.',
            hour_of_day = 4,
            minute_of_hour = 56

        )
    ]