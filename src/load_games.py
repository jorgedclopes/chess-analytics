"""
    This script loads data available locally.
    This function is to be used as:

    from src.load_games import get_games
    games = get_games('resources/game_ids.dat')
"""
import ast
import os
import warnings
from operator import itemgetter


def load_games(file):
    """Loads the games available locally.

    Args: file (str): Path to .env file with lichess token.

    Returns: games (list[dict]):

    """
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

    if len(games) is 0:
        warnings.warn("No token loaded.", ResourceWarning)
    return games
