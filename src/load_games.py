'''
    This script takes data available locally and produces some results.
'''

import os
import lichess.api
from operator import itemgetter
import json

name = 'carequinha'
user = lichess.api.user(name)


def getGames(file):
    with open(os.path.join(os.getcwd(),
                           file), 'r') as f:
        game_id_list = f.readlines()

    game_id_list = [(game_id_list[0][i:i + 8]) for i in
                    range(0, len(game_id_list[0]), 8)]

    games = list()
    for id_var in game_id_list:
        filename = "resources/JSON_database/" +\
                   id_var +\
                   ".json"
        with open(os.path.join(os.getcwd(),
                               filename), 'r') as f:
            ind_game = json.loads(f.read())
            games.append(ind_game)

    games = sorted(games,
                   key=itemgetter('createdAt'))  # [:20]
    return games
