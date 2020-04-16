import os
import lichess.api
from pprint import pprint
from setup_env import setup
import datetime


# Irrelevant with PGNs, just convenient for readability
def convert_ms_to_date(time_in_ms):
    base_datetime = datetime.datetime(1970, 1, 1)
    delta = datetime.timedelta(0, 0, 0, time_in_ms)
    return base_datetime + delta


# Doing this can take quite some time
def get_game_ids(name,
                 path_name='resources/game_ids.dat',
                 pref_type=None,
                 initial_time=None,
                 latest_time=None
                 ):
    # TODO: make test after this step

    if os.path.exists(path_name):
        print(path_name + ' exists. Reading this file.')
        return "Specifications ignored. Reading from file."

    user = lichess.api.user(name)

    token = setup()
    # pprint(TOKEN)

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
    for key in  user['perfs']:
        len_total_games += user['perfs'][key]['games']

    pprint("Total games seen: " + str(len_total_games))
    print(initial_time, latest_time, delta_time)
    print(convert_ms_to_date(initial_time),
          convert_ms_to_date(latest_time),
          convert_ms_to_date(delta_time))

    games_list = list()

    # this is not optimal...
    increment = max([int(delta_time / 100), 30 * 60 * 1000])
    for time_index in range(initial_time,
                            latest_time,
                            increment):
        print(convert_ms_to_date(time_index))

        games_generator = lichess.api.user_games(
            name,
            perfType=pref_type,
            since=time_index,
            until=time_index + increment,
            auth=token
        )

        games_list += list(games_generator)
        game_len = len(games_list)
        print("{:15d} {:06.2f} {:4d}"
              .format(time_index,
                      (time_index - initial_time) / increment,
                      game_len))

        if game_len >= len_total_games:
            break

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
