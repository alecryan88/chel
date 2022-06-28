select 
    partition_date,
    JSON_EXTRACT:gameData:game:pk::string as game_id,
    teams.value:division.id::int as division_id,
    teams.value:division.name::string as division_name,
    teams.value:id::int as team_id,
    '2022-06-28 11:47:08.586560+00:00' as last_updated_dbt
   
from NHL_DB.RAW.RAW_NHL_GAME_DATA, table(flatten(JSON_EXTRACT:gameData:teams)) teams