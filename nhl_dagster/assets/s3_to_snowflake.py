from dagster import asset
from dagster_snowflake import snowflake_resource
from nhl_dagster.partitions.partitions import daily_partitions_def

@asset(
    required_resource_keys={'snowflake'},
    partitions_def=daily_partitions_def,
    compute_kind='SQL',
    key_prefix = 'SNOWFLAKE_RAW',
    group_name = 'snowflake_raw_game_data'
)
def RAW_NHL_GAME_DATA(context, load_game_data_to_s3):
    '''
    DROP/REPLACE PARTITION FROM RAW.RAW_NHL_GAME_DATA in Snowflake
    '''
    
    partition_key = context.output_asset_partition_key()

    context.resources.snowflake.execute_query(f"""
        
        DELETE FROM RAW.RAW_NHL_GAME_DATA
        where partition_date = date('{partition_key}')
        """
    )

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