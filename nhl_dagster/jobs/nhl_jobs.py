from dagster import job, op, get_dagster_logger, In, Nothing
from nhl_dagster.ops.s3_ops import *
from nhl_dagster.ops.dbt_ops import *
from nhl_dagster.ops.snowflake_ops import *
from nhl_dagster.partitions.daily_partitions import nhl_elt_daily_config
from nhl_dagster.resources.resources import * 

@job(
    config=nhl_elt_daily_config,
    resource_defs={
        "s3": s3_resource,
        "snowflake": snowflake_resource_configured,
        "dbt": dbt_resource_configured
        }
    )
def run_elt():
    game_id_list = extract_game_ids_to_list()
    load_data = load_game_data_to_s3(game_id_list)
    delete_partition = delete_partition_from_snowflake(start=load_data)
    copy_partition = copy_partition_into_snowflake(start=delete_partition)
    dbt_run_models = dbt_run(start=copy_partition)
    dbt_test_models = dbt_test(start=dbt_run_models)