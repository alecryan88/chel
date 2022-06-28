select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    play_id as unique_field,
    count(*) as n_records

from NHL_DB.ANALYTICS.stg_game_events
where play_id is not null
group by play_id
having count(*) > 1



      
    ) dbt_internal_test