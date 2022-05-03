{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert'
    )
}}

Select  
      partition_date,
       {{ dbt_utils.surrogate_key(['game_id', 'event_id', 'period_s'])}} as play_id,
      game_id,
      game_season,
      event_id,
      players.value:player:id::string as player_id,
      players.value:playerType::string as player_type
  from (
    Select 
      partition_date,
      JSON_EXTRACT:gameData:game:pk::string as game_id,
      JSON_EXTRACT:gameData:game:season::string as game_season,
      plays.value:about:eventId::int as event_id,
      plays.value:players as players,
      plays.value:about.ordinalNum::string as period_s,
      '{{ run_started_at }}' as last_updated_dbt

    from {{source('NHL_DB_RAW', 'RAW_NHL_GAME_DATA')}}, table(flatten(JSON_EXTRACT:liveData.plays.allPlays)) plays

    {% if is_incremental() %}
    where partition_date = date('{{ var('run_date') }}')
    {% endif %}

  ), table(flatten(players)) players