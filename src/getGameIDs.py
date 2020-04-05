import os
import lichess.api
from pprint import pprint
from setup import setup
import pathlib
import datetime


def convert_ms_to_date(time_in_ms):
    base_datetime = datetime.datetime(1970, 1, 1)
    delta = datetime.timedelta(0, 0, 0, time_in_ms)
    return base_datetime + delta


def get_game_ids(name, path_name='resources/game_ids.dat', pref_type='blitz'):
    # TODO: pass also path_name with default - DONE
    # TODO: pass preferred game qualification ('blitz'), make test after this step
    # TODO: write dates in a readable/intuitive format

    if os.path.exists(path_name):
        print(path_name + ' exists. Reading this file.')
        return "From file."

    user = lichess.api.user(name)

    token = setup()
    # pprint(TOKEN)

    # print(user['perfs'].values())
    # for i in user['perfs']:
    #    print(i, "\t", user['perfs'][i])

    # time in milliseconds since Jan 1st 1970
    len_blitz_games = user['perfs'][pref_type]['games']
    initial_time = user['createdAt']
    latest_time = user['seenAt']
    delta_time = latest_time - initial_time

    pprint("Reading " + str(len_blitz_games) + " games.")
    print(initial_time, latest_time, delta_time)
    print(convert_ms_to_date(initial_time),
          convert_ms_to_date(latest_time),
          convert_ms_to_date(delta_time))

    games_list = list()

    increment = int(delta_time / 100)
    for time in range(initial_time, latest_time, increment):
        games_generator = lichess.api.user_games(
            name,
            perfType=pref_type,
            since=time,
            until=time + increment,
            auth=token
        )

        games_list += list(games_generator)
        game_len = len(games_list)
        print("{:15d} {:06.2f} {:4d} {:5d}"
              .format(time, (time - initial_time) / delta_time * 100,
                      game_len, len_blitz_games))

    # for game in games_list:
    #    print(game['id'])

    with open(path_name, 'w') as f:
        for game in games_list:
            f.writelines(game['id'])

    return "From remote."


# print(type(games))
# games_length = sum(1 for _ in games)

if __name__ == "__main__":
    get_game_ids('carequinha')
