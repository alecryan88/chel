from dagster import asset, AssetGroup
from dagster_snowflake import snowflake_resource


@asset(
    required_resource_keys={'snowflake','run_parameters'},
    compute_kind='SQL'
)
def delete_partition_from_snowflake(context):
    '''
    Delete partition = run date from snowflake.
    '''
    
    partition_key = context.resources.run_parameters['run_date']
    
    context.resources.snowflake.execute_query(f"""
        
        DELETE FROM RAW.RAW_NHL_GAME_DATA
        where partition_date = date('{partition_key}')
        """
    )

@asset(
    required_resource_keys={'snowflake', 'run_parameters'},
    compute_kind='SQL'
)
def copy_partition_into_snowflake(context, delete_partition_from_snowflake):
    '''
    Copy partition into snowflake from s3
    '''
    
    partition_key = context.resources.run_parameters['run_date']

    context.resources.snowflake.execute_query(f"""
        
        copy into RAW.RAW_NHL_GAME_DATA
        from (
        Select 
                METADATA$FILENAME as file_name,
                date(split_part(split_part(METADATA$FILENAME, '/', 2),'=',2)) as partition_date,
                split_part(split_part(METADATA$FILENAME, '/', 3), '.',1) as game_id,
                $1 as json_extract
                
        from @RAW.RAW_NHL_GAME_DATA
        )
        pattern = '.*partition_date={partition_key}.*.json'
        force = TRUE;
        """
    )