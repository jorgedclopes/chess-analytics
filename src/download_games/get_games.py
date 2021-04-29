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
from typing import List
import rootpath

import lichess.api
from lichess.format import SINGLE_PGN
from src.download_games.setup_env import setup


def convert_ms_to_date(time_in_ms: int) -> datetime.datetime:
    """
    Convert epoch time in ms to readable datetime format.

    Parameters
    ----------
    time_in_ms : int
        current epoch time in ms.

    Returns
    -------
        Datetime
            Time in a readable format.
    """
    base_datetime = datetime.datetime(1970, 1, 1)
    delta = datetime.timedelta(0, 0, 0, time_in_ms)
    return base_datetime + delta


def save_to_file(game: list,
                 save_dir: str,
                 save_file: str):
    """Save game from lichess.org in file.

    Parameters
    ----------
    game : list
        data about all downloaded chess games.
    save_dir : str
        Folder in which the games will be saved.
    save_file : str
        File in which the games will be saved.
    Returns
    -------
        None

    """
    filename = os.path.join(save_dir, save_file + '.pgn')
    with open(filename, 'w') as file:
        file.write("".join(game))


def download_games(name: str,
                   db_dir: str = 'resources',
                   perf_type: str = None,
                   time_period: tuple = (None, None),
                   is_rated: bool = True,
                   token: str = None
                   ) -> None:
    """Fetch token from .env file.

    Parameters
    ----------
    name : str
        Path to .env file with lichess token.
    db_dir : str
        Folder to which write the file.
    perf_type : str, list
        filter time control
        To download all several types, provide them as a list.
        Default: None
    time_period : tuple
        time window for games to download.
        Default: beginning of user account, latest account update time.
    is_rated : bool
        whether to download rated games, non-rated or all.
        Default: True
    token : str
        Token to authenticate to lichess.
        Speeds up downloading the games.
        Default: None

    Returns
    -------
        None
    """

    if os.path.exists(os.path.join(db_dir, name + ".pgn")):
        warnings.warn('PGN database already downloaded.',
                      ResourceWarning)
        return

    if not os.path.isdir(db_dir):
        Path(db_dir).mkdir(parents=True, exist_ok=False)

    user = lichess.api.user(name)

    # time in milliseconds since Jan 1st 1970
    initial_time, latest_time = time_period
    if initial_time is None:
        initial_time = user['createdAt']
    if latest_time is None:
        latest_time = user['seenAt']
    delta_time = latest_time - initial_time

    len_total_games = 0
    for key in user['perfs']:
        part_games = user['perfs'][key].get('games', 0)
        len_total_games += part_games

    pprint("Total games seen: " + str(len_total_games))
    print(initial_time, latest_time, delta_time)
    print(convert_ms_to_date(initial_time),
          convert_ms_to_date(latest_time))

    games_list: List[str] = list()

    time_30min = 30 * 60 * 1000
    increment = max([int(delta_time / 100), time_30min])

    for time_index in range(initial_time,
                            latest_time,
                            increment):
        print(convert_ms_to_date(time_index),
              "\t\t",
              convert_ms_to_date(time_index + increment))

        games_generator = lichess.api.user_games(
            name,
            perfType=perf_type,
            since=time_index,
            until=time_index + increment,
            rated="true" if is_rated else "false",
            clocks="true",
            format=SINGLE_PGN,
            auth=token
        )

        games_list += list(games_generator)
        game_len = len(games_list)
        print("{:15d} {:06.2f} {:4d}"
              .format(time_index,
                      (time_index - initial_time) / increment,
                      game_len))

    save_to_file(games_list, db_dir, name)
    # for game in games_list:
    #     save_to_file(game, db_dir)


if __name__ == '__main__':  # pragma: no cover
    root_path = rootpath.detect()
    path = os.path.join(root_path, '/resources')
    auth = setup(path=path)
    user_name = 'carequinha'
    user_stats = lichess.api.user(user_name)
    time_creation = user_stats['createdAt']
    time_last_seen = user_stats['seenAt']
    inc = int(time_last_seen - time_creation / 100)
    time_mock = time_creation + inc

    # this is a mock to demo how to use this function, the timeframes are very small
    download_games(user_name,
                   db_dir=path,
                   perf_type="blitz",
                   time_period=(time_creation, time_mock),
                   token=auth)
