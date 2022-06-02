from dagster import daily_partitioned_config
from datetime import datetime

@daily_partitioned_config(start_date=datetime(2020, 1, 1))
def nhl_elt_daily_config(start: datetime, _end: datetime):
    return {
        "resources": {
            "run_date": {
                "config": start.strftime("%Y-%m-%d")
            }
        }
    }