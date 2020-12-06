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
from lichess.format import SINGLE_PGN
from src.setup_env import setup


def convert_ms_to_date(time_in_ms: int):
    """
    Convert epoch time in ms to readable datetime format.

    Args:
        time_in_ms (int): current epoch time in ms.

    Returns
    -------
        Datetime
            Time in a readable format.
    """
    base_datetime = datetime.datetime(1970, 1, 1)
    delta = datetime.timedelta(0, 0, 0, time_in_ms)
    return base_datetime + delta


def save_to_file(game,
                 save_dir,
                 save_file):
    """Save game in file.

    Args:
        game (list): data about all downloaded chess games.
        save_dir (str): Folder in which the games will be saved.
        save_file (str): File in which the games will be saved.
    Returns:
        None

    """
    filename = os.path.join(save_dir, save_file + '.pgn')
    if os.path.exists(filename):
        with open(filename, 'a') as file:
            file.write("".join(game))
    else:
        with open(filename, 'w') as file:
            file.write("".join(game))


def download_games(name: str,
                   db_dir: str = 'resources',
                   perf_type: str = None,
                   initial_time: int = None,
                   latest_time: int = None,
                   is_rated: bool = True,
                   mock: bool = False
                   ) -> None:
    """Function to fetch token from .env file.

    Args:
        name (str): Path to .env file with lichess token.
        db_dir (str): Setup and make folder if it doesn't
            already exist. Default = resources
        pref_type (str): filter time control
            To download all several types,
            provide them as a list.
            Default = None
        initial_time : int
            beginning of window to download games.
            Default: beginning of user account.
        latest_time : int
            end of window to download games.
            Default: latest account update time.
        is_rated: whether to download rated games, non-rated or all

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

    token = setup(path="resources/")

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
          convert_ms_to_date(latest_time))

    games_list = list()

    time_30min = 30 * 60 * 1000
    increment = max([int(delta_time / 100), time_30min])
    if mock:
        latest_time = initial_time + increment

    for time_index in range(initial_time,
                            latest_time,
                            increment):
        print(convert_ms_to_date(time_index).__str__() +
              "\t\t" +
              convert_ms_to_date(time_index + increment).__str__())

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
    download_games('carequinha',
                   perf_type="blitz")
