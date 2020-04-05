import os
import lichess.api
from pprint import pprint
from setup import setup
import pathlib


def get_game_ids(name):
    # TODO: pass also path_name with default
    # TODO: pass prefered game qualification ('blitz'), make test after this step
    # TODO: write dates in a readable/intuitive format
    path_name = 'resources/game_ids.dat'
    if os.path.exists(path_name):
        print(path_name + ' exists. Reading this file.')
        return "From file."

    user = lichess.api.user(name)

    TOKEN = setup()
    # pprint(TOKEN)

    # print(user['perfs'].values())
    # for i in user['perfs']:
    #    print(i, "\t", user['perfs'][i])

    # time in miliseconds since Jan 1st 1970
    len_blitz_games = user['perfs']['blitz']['games']
    initial_time = user['createdAt']
    latest_time = user['seenAt']
    delta_time = latest_time - initial_time

    pprint("Reading " + str(len_blitz_games) + " games.")
    print(initial_time, latest_time, delta_time)

    games_list = list()

    increment = int(delta_time / 100)
    for time in range(initial_time, latest_time, increment):
        games_generator = lichess.api.user_games(
            name,
            perfType='blitz',
            since=time,
            until=time + increment,
            auth=TOKEN
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
