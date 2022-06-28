select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select event_id
from NHL_DB.ANALYTICS.stg_game_events_players
where event_id is null



      
    ) dbt_internal_test