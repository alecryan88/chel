
    
    

select
    play_id as unique_field,
    count(*) as n_records

from NHL_DB.ANALYTICS.stg_game_events
where play_id is not null
group by play_id
having count(*) > 1


