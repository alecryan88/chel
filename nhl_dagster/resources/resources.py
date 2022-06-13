from dagster_aws.s3.resources import s3_resource
from dagster_dbt import dbt_cli_resource
from dagster_snowflake import snowflake_resource
import os


snowflake_resource_configured = snowflake_resource.configured({
    'account': os.environ['SNOWFLAKE_ACCOUNT'],
    'user': os.environ['SNOWFLAKE_USER'], 
    'password': os.environ['SNOWFLAKE_PASSWORD'],
    'database': os.environ['SNOWFLAKE_DATABASE'],
    'warehouse': os.environ['SNOWFLAKE_WAREHOUSE']
    }
)

dbt_resource_configured = dbt_cli_resource.configured({
    'profiles_dir': os.environ['DBT_DIR'], 
    'project_dir':  os.environ['DBT_DIR'],
    'target': 'prod'
    }
)