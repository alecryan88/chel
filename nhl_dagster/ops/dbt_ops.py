from dagster import op, get_dagster_logger, In, Nothing
from dagster_dbt import dbt_test_op, dbt_run_op

@op(
    required_resource_keys={'dbt', 'run_date'}, 
    ins={"start": In(Nothing)}
    )
def dbt_run(context):
    date = context.resources.run_date
    context.resources.dbt.run(vars={"run_date": date})


@op(
    required_resource_keys={'dbt', 'run_date'}, 
    ins={"start": In(Nothing)}
    )
def dbt_test(context):
    date = context.resources.run_date
    context.resources.dbt.test(vars={"run_date": date})


@op(
    required_resource_keys={'dbt', 's3'}, 
    ins={"start": In(Nothing)}
    )
def load_dbt_manifest_to_s3(context):
    '''
    Loads dbt manifest in specified location to bucket in s3.

    '''
    context.resources.s3.put_object(
        Body='./nhl_dbt/target/manifest.json',
        Bucket='nhl-prod-dbt-manifest',
        Key='manifest.json'
    )