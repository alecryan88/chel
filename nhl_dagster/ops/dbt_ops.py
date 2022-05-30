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