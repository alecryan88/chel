
  create or replace  view NHL_DB.ANALYTICS.stg_game_officials
  
   as (
    Select 
    partition_date,
    JSON_EXTRACT:gameData:game:pk::string as game_id,
    JSON_EXTRACT:gameData:game:season::string as game_season,
    trim(split_part(officials.value:official.fullName::string,' ',1))  as official_first_name,
    trim(split_part(officials.value:official.fullName::string,' ',2))  as official_last_name,
    officials.value:official.id::int as official_id,
    officials.value:officialType::string as official_type,
    '2022-06-28 11:47:08.586560+00:00' as last_updated_dbt
    
from NHL_DB.RAW.RAW_NHL_GAME_DATA, table(flatten(JSON_EXTRACT:liveData:boxscore:officials)) officials
  );
