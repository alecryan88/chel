
  create or replace  view NHL_DB.ANALYTICS.stg_game_metadata
  
   as (
    Select
    partition_date,
    JSON_EXTRACT:gameData:game:season::string as game_season,
    JSON_EXTRACT:gameData:game:pk::string as game_id,
    JSON_EXTRACT:gameData:game:type::string as game_type,
    JSON_EXTRACT:gameData:teams:away.id as away_team_id,
    JSON_EXTRACT:gameData:teams:home.id as home_team_id,
    JSON_EXTRACT:gameData:datetime:dateTime::timestamp as game_start,
    JSON_EXTRACT:gameData:datetime:endDateTime::timestamp as game_end,
    JSON_EXTRACT:gameData:status:abstractGameState::string as game_state,
    '2022-06-28 11:47:08.586560+00:00' as last_updated_dbt

from NHL_DB.RAW.RAW_NHL_GAME_DATA
  );
