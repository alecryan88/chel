{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert'
    )
}}


select 
    partition_date,
    JSON_EXTRACT:gameData:game:pk::string as game_id,
    teams.value:division.id::int as division_id,
    teams.value:division.name::string as division_name,
    teams.value:id::int as team_id,
    '{{ run_started_at }}' as last_updated_dbt
   
from {{source('NHL_DB_RAW', 'RAW_NHL_GAME_DATA')}}, table(flatten(JSON_EXTRACT:gameData:teams)) teams

{% if is_incremental() %}
where partition_date = date('{{ var('run_date') }}')
{% endif %}