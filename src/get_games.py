"""
  This file has the function to fetch token from .env file.
  Unless you are developing, there is no point in
  calling this function.
"""
import os
import warnings
from pathlib import Path
from pprint import pprint
import datetime
import lichess.api
from src.setup_env import setup


def convert_ms_to_date(time_in_ms):
    """Convert epoch time in ms to readable datetime format.

    Args:
        time_in_ms (str): current epoch time in ms.

    Returns:
        time (datetime): returns the time in a readable format.
    """
    base_datetime = datetime.datetime(1970, 1, 1)
    delta = datetime.timedelta(0, 0, 0, time_in_ms)
    return base_datetime + delta


def save_to_file(game,
                 save_path):
    """Save game in file.

    Args:
        game (str): data about one chess game.
        save_path (str): Folder in which the game will be saved.

    Returns:
        None
    """
    filename = save_path + '/' + game['id'] + '.pgn'
    with open(filename, 'w') as file:
        file.write(str(game))


def download_games(name,
                   db_dir='resources/PGN_database',
                   pref_type=None,
                   initial_time=None,
                   latest_time=None,
                   is_rated=True,
                   ) -> None:
    """Function to fetch token from .env file.

    Args:
        name (str): Path to .env file with lichess token.
        db_dir (str): Setup and make folder if it doesn't
            already exist. Default = resources/PGN_database
        pref_type (str): filter time control
            to download.
            To download all several types,
            provide them as a list.
            Default = None
        initial_time (int): beginning of window
            to download games.
            Default: beginning of user account.
        latest_time (int): end of window
            to download games.
            Default: latest account update time.
        is_rated (bool): filter rated games.
            Default: True (Rated only)

    Returns:
        None
    """

    if os.path.isdir(db_dir):
        warnings.warn('PGN database already downloaded.',
                      ResourceWarning)
        return

    Path(db_dir).mkdir(parents=True, exist_ok=False)

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

    for game in games_list:
        save_to_file(game, db_dir)


if __name__ == '__main__':  # pragma: no cover
    download_games('carequinha',
                   pref_type='blitz',
                   is_rated=True)
