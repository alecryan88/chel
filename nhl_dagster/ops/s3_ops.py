import requests
import io
from dagster import op, get_dagster_logger, In, Nothing
from dagster_aws.s3.resources import s3_resource

@op(required_resource_keys={'s3', 'run_date'})
def extract_game_ids_to_list(context):
    '''
    Extzracts the game_ids on the execution_date and returns them in a game_id_list.
    '''

    date = context.resources.run_date

    game_id_list = []
    
    request_url = f'https://statsapi.web.nhl.com/api/v1/schedule?startDate={date}&endDate={date}'
    r = requests.get(request_url) 
    j = r.json()
    
    dates = j['dates']
    
    for day in dates:
        games = day['games']
        for game in games:
            game_id = game['gamePk']
            game_id_list.append(game_id)

    get_dagster_logger().info(f'Game_ids {game_id_list}')

    return game_id_list

   
@op(required_resource_keys={'s3', 'run_date'})
def load_game_data_to_s3(context, game_id_list):
    '''
    Load game_data to s3 in JSON format.
    '''

    date = context.resources.run_date

    for game_id in game_id_list:
        r = requests.get(f'https://statsapi.web.nhl.com/api/v1/game/{game_id}/feed/live')
    
        #Store JSON respose
        json = io.BytesIO(r.content)

        context.resources.s3.put_object(
            Body=json,
            Bucket='nhl-analytics',
            Key=f'nhl-game-data/partition_date={date}/{game_id}.json'
        )