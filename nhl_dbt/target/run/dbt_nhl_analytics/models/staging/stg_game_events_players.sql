
  create or replace  view NHL_DB.ANALYTICS.stg_game_events_players
  
   as (
    Select  
      partition_date,
       md5(cast(coalesce(cast(game_id as 
    varchar
), '') || '-' || coalesce(cast(event_id as 
    varchar
), '') || '-' || coalesce(cast(period_s as 
    varchar
), '') as 
    varchar
)) as play_id,
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
      '2022-06-28 11:47:08.586560+00:00' as last_updated_dbt

    from NHL_DB.RAW.RAW_NHL_GAME_DATA, table(flatten(JSON_EXTRACT:liveData.plays.allPlays)) plays

  ), table(flatten(players)) players
  );
