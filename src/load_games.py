"""
    This script loads data available locally.
    This function is to be used as:

    from src.load_games import get_games
    games = get_games('resources/PGN_database')
"""
import os
import warnings
from operator import itemgetter

import chess.pgn


def flatten(arg_list):
    return [item for sublist in arg_list for item in sublist]


def load_games(path: str = 'resources/',
               is_rated: bool = None):
    """Loads the games available locally.

    Parameters
    ----------
        path : str
            path to games database folder.
            Default: resources/PGN_database

        is_rated : bool
            filter rated games.
            {True -> only rated,
             False -> only casual,
             None -> all games}
            Default: None

    Returns
    -------
        List[dict]
            list of games in DB, sorted by date.

    """

    fname = None
    if os.path.isdir(path):
        fname = flatten(list(map(lambda x:
                                 list(map(lambda y:
                                          os.path.join(x[0], y),
                                          x[2])),
                                 os.walk(path))))

    elif os.path.exists(path):
        fname = [path]

    flatten(fname)
    print(fname)

    games = list()
    for file in fname:
        with open(file, 'r') as f:
            while True:
                game = chess.pgn.read_game(f)
                if game is None:
                    break
                games.append(game)

    print(games[0])
    games = sorted(games,
                   key=itemgetter('UTCDate'))

    if len(games) == 0:
        warnings.warn("No games found in this folder.",
                      ResourceWarning)
    return games


if __name__ == '__main__':  # pragma: no cover
    load_games('resources/database.pgn')