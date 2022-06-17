from dagster import asset
from nhl_dagster.partitions.partitions import daily_partitions_def
import requests
import io


@asset(
    partitions_def=daily_partitions_def,
    compute_kind='python'
)
def extract_game_ids_to_list(context):
    '''
    Extzracts the game_ids on the execution_date and returns them in a game_id_list.
    '''

    partition_key = context.output_asset_partition_key()

    game_id_list = []
    
    request_url = f'https://statsapi.web.nhl.com/api/v1/schedule?startDate={partition_key}&endDate={partition_key}'
    r = requests.get(request_url) 
    j = r.json()
    
    dates = j['dates']
    
    for day in dates:
        games = day['games']
        for game in games:
            game_id = game['gamePk']
            game_id_list.append(game_id)

    return game_id_list

   
@asset(
    required_resource_keys={'s3'},
    partitions_def=daily_partitions_def,
    compute_kind='python'
)
def load_game_data_to_s3(context, extract_game_ids_to_list):
    '''
    Load game_data to s3 in JSON format.
    '''

    partition_key = context.output_asset_partition_key()
    

    for game_id in extract_game_ids_to_list:
        r = requests.get(f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/feed/live')
    
        #Store JSON respose
        json = io.BytesIO(r.content)

        context.resources.s3.put_object(
            Body=json,
            Bucket='nhl-analytics',
            Key=f'nhl-game-data/partition_date={partition_key}/{game_id}.json'
        )