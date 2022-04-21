from dagster import asset, AssetGroup,  DailyPartitionsDefinition
from dagster_snowflake import snowflake_resource

daily_partitions_def = DailyPartitionsDefinition(start_date="2020-01-01")

@asset(
    required_resource_keys={'snowflake'},
    partitions_def=daily_partitions_def,
    compute_kind='SQL'
)
def delete_partition_from_snowflake(context):
    '''
    Delete partition = run date from snowflake.
    '''
    
    partition_key = context.output_asset_partitions_time_window()
    
    context.resources.snowflake.execute_query(f"""
        
        DELETE FROM RAW.RAW_NHL_GAME_DATA
        where partition_date = date('{partition_key}')
        """
    )

@asset(
    required_resource_keys={'snowflake'},
    partitions_def=daily_partitions_def,
    compute_kind='SQL'
)
def copy_partition_into_snowflake(context, delete_partition_from_snowflake):
    '''
    Copy partition into snowflake from s3
    '''
    
    partition_key = context.output_asset_partitions_time_window()

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