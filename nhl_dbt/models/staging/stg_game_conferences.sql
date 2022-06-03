{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert'
    )
}}

--test
Select distinct
    partition_date,
    JSON_EXTRACT:gameData:game:pk::string as game_id,
    teams.value:conference.id::integer as conference_id,
    teams.value:conference.name::string as conference_name,
    teams.value:division.id::int as division_id,
    '{{ run_started_at }}' as last_updated_dbt
   
from {{source('NHL_DB_RAW', 'RAW_NHL_GAME_DATA')}}, table(flatten(JSON_EXTRACT:gameData:teams)) teams

{% if is_incremental() %}
where partition_date = date('{{ var('run_date') }}')
{% endif %}