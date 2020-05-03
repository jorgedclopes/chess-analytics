import os
from pathlib import Path
from pprint import pprint
import datetime
import lichess.api
from src.setup_env import setup


def convert_ms_to_date(time_in_ms):
    base_datetime = datetime.datetime(1970, 1, 1)
    delta = datetime.timedelta(0, 0, 0, time_in_ms)
    return base_datetime + delta


def save_to_file(game,
                 save_path):
    filename = save_path + '/' + game['id'] + '.pgn'
    with open(filename, 'w') as file:
        file.write(str(game))


def download_games(name,
                   path_name='resources/game_ids.dat',
                   db_dir='resources/PGN_database',
                   pref_type=None,
                   initial_time=None,
                   latest_time=None,
                   is_rated=True,
                   ):

    Path(db_dir).mkdir(parents=True, exist_ok=True)
    if os.path.exists(path_name):
        print(path_name + ' exists. Reading this file.')
        return "Specifications ignored. Reading from file."

    user = lichess.api.user(name)

    token = setup()

    # print(user['perfs'].values())
    # for i in user['perfs']:
    #    print(i, "\t", user['perfs'][i])

    # time in milliseconds since Jan 1st 1970
    if initial_time is None:
        initial_time = user['createdAt']
    if latest_time is None:
        latest_time = user['seenAt']
    delta_time = latest_time - initial_time

    len_total_games = 0
    for key in user['perfs']:
        len_total_games += user['perfs'][key]['games']

    pprint("Total games seen: " + str(len_total_games))
    print(initial_time, latest_time, delta_time)
    print(convert_ms_to_date(initial_time),
          convert_ms_to_date(latest_time),
          convert_ms_to_date(delta_time))

    games_list = list()

    time_30min = 30 * 60 * 1000
    increment = max([int(delta_time / 100), time_30min])
    for time_index in range(initial_time,
                            latest_time,
                            increment):
        print(convert_ms_to_date(time_index))

        games_generator = lichess.api.user_games(
            name,
            perfType=pref_type,
            since=time_index,
            until=time_index + increment,
            rated=is_rated,
            auth=token
        )

        games_list += list(games_generator)
        game_len = len(games_list)
        print("{:15d} {:06.2f} {:4d}"
              .format(time_index,
                      (time_index - initial_time) / increment,
                      game_len))

    with open(path_name, 'w') as f:
        for game in games_list:
            f.writelines(game['id'])
            save_to_file(game, db_dir)

    return "From remote."

