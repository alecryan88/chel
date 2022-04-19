{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert'
    )
}}

Select 
    partition_date,
    JSON_EXTRACT:gameData:game:pk::string as game_id,
    'Away' as home_away_status,
    JSON_EXTRACT:liveData:boxscore:teams:away:team:id as team_id,
    case 
        when ARRAY_CONTAINS( players.value:person:id, JSON_EXTRACT:liveData:boxscore:teams:away:scratches::array) = TRUE then 'Scratched' 
        else 'Active'
    end active_status,
    players.value:person:id as player_id,
    players.value:jerseyNumber::varchar as jersey_number,
    players.value:person:fullName::varchar as full_name,
    players.value:person:rosterStatus::varchar as roster_status,
    players.value:person:shootsCatches::varchar as shoots_catches,
    players.value:position:abbreviation::varchar as pos_abv,
    players.value:position:code::varchar as pos_code,
    players.value:position:name::varchar as pos_name,
    players.value:position:type::varchar as pos_type

    
from {{source('NHL_DB_RAW', 'RAW_NHL_GAME_DATA')}}, table(flatten(JSON_EXTRACT:liveData:boxscore:teams:away:players)) players

{% if is_incremental() %}
where partition_date = date({{ var('run_date') }})
{% endif %}

union

Select 
    partition_date,
    JSON_EXTRACT:gameData:game:pk::string as game_id,
    'Home' as home_away_status,
    JSON_EXTRACT:liveData:boxscore:teams:home:team:id as team_id,
    case 
        when ARRAY_CONTAINS( players.value:person:id, JSON_EXTRACT:liveData:boxscore:teams:home:scratches::array) = TRUE then 'Scratched' 
        else 'Active'
    end active_status,
    players.value:person:id as player_id,
    players.value:jerseyNumber::varchar as jersey_number,
    players.value:person:fullName::varchar as full_name,
    players.value:person:rosterStatus::varchar as roster_status,
    players.value:person:shootsCatches::varchar as shoots_catches,
    players.value:position:abbreviation::varchar as pos_abv,
    players.value:position:code::varchar as pos_code,
    players.value:position:name::varchar as pos_name,
    players.value:position:type::varchar as pos_type

    
from {{source('NHL_DB_RAW', 'RAW_NHL_GAME_DATA')}}, table(flatten(JSON_EXTRACT:liveData:boxscore:teams:home:players)) players

{% if is_incremental() %}
where partition_date = date('{{ var('run_date') }}')
{% endif %}