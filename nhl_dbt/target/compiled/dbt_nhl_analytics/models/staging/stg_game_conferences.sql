Select distinct
    partition_date,
    JSON_EXTRACT:gameData:game:pk::string as game_id,
    teams.value:conference.id::integer as conference_id,
    teams.value:conference.name::string as conference_name,
    teams.value:division.id::int as division_id,
    '2022-06-28 11:47:08.586560+00:00' as last_updated_dbt
   
from NHL_DB.RAW.RAW_NHL_GAME_DATA, table(flatten(JSON_EXTRACT:gameData:teams)) teams