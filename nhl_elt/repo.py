from dagster import repository
from nhl_elt.jobs.stage_data_in_s3 import * 
from nhl_elt.jobs.load_data_to_snowflake import * 
from nhl_elt.jobs.dbt_transforms import *

@repository
def nhl_elt_prod():
    return [
        stage_game_data,
        load_data_to_snowflake,
        dbt_transforms
    ]