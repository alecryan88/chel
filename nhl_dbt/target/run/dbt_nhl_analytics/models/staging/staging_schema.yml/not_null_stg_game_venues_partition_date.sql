select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select partition_date
from NHL_DB.ANALYTICS.stg_game_venues
where partition_date is null



      
    ) dbt_internal_test