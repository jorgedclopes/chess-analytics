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

    Parameters
    ----------
        time_in_ms (int) : current epoch time in ms.

    Returns
    -------
        Datetime
            Time in a readable format.
    """
    base_datetime = datetime.datetime(1970, 1, 1)
    delta = datetime.timedelta(0, 0, 0, time_in_ms)
    return base_datetime + delta


def download_games(name,
                   dest_file='resources/database.pgn',
                   pref_type=None,
                   initial_time=None,
                   latest_time=None
                   ) -> None:
    """
    Function to fetch token from .env file.

    Parameters
    ----------
        name : str
            Path to .env file with lichess token.
        dest_file : str
            Setup and make folder if it doesn't
            already exist. Default = resources/database.pgn
        pref_type : str
            filter time control to download.
            To download all several types,
            provide them as a list.
            Default = None
        initial_time : str
            beginning of window to download games.
            Default: beginning of user account.
        latest_time : str
            end of window to download games.
            Default: latest account update time.

    Returns
    -------
        None
    """

    if os.path.exists(dest_file):
        warnings.warn('PGN database already downloaded.',
                      ResourceWarning)
        return

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
            auth=token,
            format=SINGLE_PGN
        )

        games_list += list(games_generator)
        game_len = len(games_list)
        print("{:15d} {:06.2f} {:4d}"
              .format(time_index,
                      (time_index - initial_time) / increment,
                      game_len))

    for game in games_list:
        with open(dest_file, 'a') as file:
            file.write(str(game))


if __name__ == '__main__':  # pragma: no cover
    download_games('carequinha',
                   pref_type='blitz')
