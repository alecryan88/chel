from dagster import op, get_dagster_logger, In, Nothing
from dagster_dbt import dbt_test_op, dbt_run_op

@op(
    config_schema={'run_date': str}, 
    required_resource_keys={'dbt'}, 
    ins={"start": In(Nothing)}
    )
def dbt_run(context):
    context.resources.dbt.run()


@op(
    config_schema={'run_date': str}, 
    required_resource_keys={'dbt'}, 
    ins={"start": In(Nothing)}
    )
def dbt_test(context):
    context.resources.dbt.test()