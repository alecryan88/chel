from dagster import daily_partitioned_config
from datetime import datetime

@daily_partitioned_config(start_date=datetime(2020, 1, 1))
def nhl_elt_daily_config(start: datetime, _end: datetime):
    return {
        "ops": {
            "extract_game_ids_to_list": {"config": {"date": start.strftime("%Y-%m-%d")}},
            "load_game_data_to_s3": {"config": {"date": start.strftime("%Y-%m-%d")}},
            "delete_partition_from_snowflake": {"config": {"date": start.strftime("%Y-%m-%d")}},
            "copy_partition_into_snowflake": {"config": {"date": start.strftime("%Y-%m-%d")}},
            "dbt_run": {"config": {"run_date": start.strftime("%Y-%m-%d")}},
            "dbt_test": {"config": {"run_date": start.strftime("%Y-%m-%d")}}
        }
    }