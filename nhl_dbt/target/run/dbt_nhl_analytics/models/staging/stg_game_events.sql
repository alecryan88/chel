
  create or replace  view NHL_DB.ANALYTICS.stg_game_events
  
   as (
    Select 
    partition_date,
    md5(cast(coalesce(cast(JSON_EXTRACT:gameData:game:pk::string as 
    varchar
), '') || '-' || coalesce(cast(plays.value:about:eventId::int as 
    varchar
), '') || '-' || coalesce(cast(plays.value:about.ordinalNum::string  as 
    varchar
), '') as 
    varchar
)) as play_id,
    JSON_EXTRACT:gameData:game:pk::string as game_id,
    plays.value:about:dateTime::timestamp as event_timestamp,
    plays.value:about:eventId::int as event_id,
    plays.value:team.id:: int as event_team_id,
    plays.value:coordinates.x::int as x_coor,
    plays.value:coordinates.y::int as y_coor,
    plays.value:result.description::string as description,
    plays.value:result.event::string as event,
    plays.value:result.eventCode::string as event_code,
    plays.value:result.eventTypeId::string as event_type_id,
    plays.value:about.period::int as period,
    plays.value:about.periodType::string as period_type,
    plays.value:about.ordinalNum::string as period_s,
    '2022-06-28 11:47:08.586560+00:00' as last_updated_dbt

from NHL_DB.RAW.RAW_NHL_GAME_DATA, table(flatten(JSON_EXTRACT:liveData.plays.allPlays)) plays
  );
