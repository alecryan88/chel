
  create or replace  view NHL_DB.ANALYTICS.stg_game_venues
  
   as (
    Select 
    partition_date,
    JSON_EXTRACT:gameData:game:pk::string as game_id,
    teams.value:id::int as team_id,
    teams.value:venue.id::int as  venue_id,
    teams.value:venue.city::string as venue_city,
    teams.value:venue.name::string as venue_name,
    teams.value:venue:timeZone.id::string as venue_timezone,
    teams.value:venue:timeZone.offset::int as venue_timezone_offset,
    '2022-06-28 11:47:08.586560+00:00' as last_updated_dbt
   
from NHL_DB.RAW.RAW_NHL_GAME_DATA, table(flatten(JSON_EXTRACT:gameData:teams)) teams
  );
