"""
    This script takes data available locally and produces some results.
"""
import ast
import os
from operator import itemgetter
import lichess.api


name = 'carequinha'
user = lichess.api.user(name)


def load_games(file):
    with open(os.path.join(os.getcwd(),
                           file), 'r') as f:
        game_id_list = f.readlines()

    game_id_list = [(game_id_list[0][i:i + 8]) for i in
                    range(0, len(game_id_list[0]), 8)]

    games = list()
    for id_var in game_id_list:
        filename = "resources/PGN_database/" +\
                   id_var +\
                   ".pgn"
        with open(os.path.join(os.getcwd(),
                               filename), 'r') as f:
            ind_game = ast.literal_eval(f.read())
            games.append(ind_game)

    games = sorted(games,
                   key=itemgetter('createdAt'))  # [:20]
    return games
