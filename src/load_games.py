"""
    This script loads data available locally.
    This function is to be used as:

    from src.load_games import get_games
    games = get_games('resources/PGN_database')
"""
import ast
import os
import warnings
from operator import itemgetter


def load_games(path: str = 'resources/PGN_database',
               is_rated: bool = None):
    """Loads the games available locally.

    Args:
        :param path: (str) : path to games database folder.
            Default: resources/PGN_database

        :param is_rated: bool : filter rated games.
            {True -> only rated,
             False -> only casual,
             None -> all games}
            Default: None

    Returns:
        games (list[dict]): list of games in DB, sorted by date.

    """

    games = list()
    for file in os.listdir(path):
        with open(os.path.join(path,
                               file), 'r') as f:
            ind_game = ast.literal_eval(f.read())
            games.append(ind_game)

    games = sorted(games,
                   key=itemgetter('createdAt'))  # [:20]

    if is_rated is None:
        game_list = games
    else:
        game_list = list(filter(
            lambda game: game['rated'] == is_rated,
            games))

    if len(game_list) == 0:
        warnings.warn("No games found in this folder.",
                      ResourceWarning)
    return game_list
