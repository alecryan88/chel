from dagster_aws.s3.resources import s3_resource
from dagster_dbt import dbt_cli_resource
from dagster_snowflake import snowflake_resource


snowflake_resource_configured = snowflake_resource.configured({
    'account': 'pua88554',
    'user':'flyers88', 
    'password':'VampireWeekend2021',
    'database': 'NHL_DB',
    'warehouse': 'NHL_ANALYTICS'
    }
)

dbt_resource_configured = dbt_cli_resource.configured({
    'profiles_dir': './nhl_dbt', 
    'project_dir': './nhl_dbt',
    'target': 'prod'
    }
)