"""
    This script loads data available locally.
    This function is to be used as:

    from src.load_games import get_games
    games = get_games('resources/PGN_database')
"""
import os
import warnings
from operator import itemgetter
import collections

import chess.pgn


def flatten_list(arg_list):
    return [item for sublist in arg_list
            for item in sublist]


def flatten_dict(arg_dict):
    items = []
    for k, v in arg_dict.items():
        new_key = k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten_dict(v).items())
        else:
            items.append((new_key, v))
    return dict(items)


def load_games(path: str = 'resources/'):
    """Loads the games available locally.

    Parameters
    ----------
        path : str
            path to games database folder.
            Default: resources/PGN_database

    Returns
    -------
        List[dict]
            list of games in DB, sorted by date.

    """

    fname = None
    if os.path.isdir(path):
        fname = flatten_list(
            list(
                map(lambda x:
                    list(map(lambda y:
                             os.path.join(x[0], y), x[2])),
                    os.walk(path)))
        )

    elif os.path.exists(path):
        fname = [path]

    flatten_list(fname)

    games = list()
    for file in fname:
        with open(file, 'r') as f:
            while True:
                game = chess.pgn.read_game(f)
                if game is None:
                    break
                game_dict = flatten_dict(game.headers.__dict__)
                game_dict["moves"] = \
                    [move.__str__()
                     for move in game.mainline_moves()]
                games.append(game_dict)

    games = sorted(games,
                   key=itemgetter('UTCDate'))

    if len(games) == 0:
        warnings.warn("No games found in this folder.",
                      ResourceWarning)
    return games


if __name__ == '__main__':  # pragma: no cover
    load_games('resources/database.pgn')
