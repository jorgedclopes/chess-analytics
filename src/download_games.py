import os
import warnings
import lichess.api
import json

from lichess.format import PGN, JSON
from get_game_ids import get_game_ids
from setup_env import setup


warnings.simplefilter('always')


def get_game_filename(file_id: str,
                      token: str,
                      input_format: str,
                      save_path='resources/JSON_database',
                      retries=5
                      ):
    if input_format == 'JSON':
        input_format = JSON
        filename = save_path + '/' + file_id + '.json'
    elif input_format == 'PGN':
        input_format = PGN
        filename = save_path + '/' + file_id + '.pgn'
    else:
        raise NameError('No valid format.')

    if not os.path.exists(filename):
        game = lichess.api.game(file_id,
                                format=input_format,
                                auth=token)

        print("File " +
              filename +
              " does not exist yet. Downloading...")
        for i in range(retries):
            try:
                with open(filename, 'w') as f:
                    if input_format == PGN:
                        f.write(str(game))
                    elif input_format == JSON:
                        json.dump(game, f)
                    # the else is taken care of
                    # input_format condition
                    break
            except FileNotFoundError:
                warnings.warn("FileNotFoundError. Attempt "
                              + str(i) +
                              "of " + str(retries) + ".",
                              ResourceWarning)
            if i == retries - 1:
                print("File couldn't be downloaded. " +
                      "Maximum number of attempts reached. " +
                      "Moving on.")
    else:
        print("File " +
              filename +
              " already exists. Not overwritten.")
        with open(filename, 'r') as file:
            game = file.read()

    return game, filename
    # what if file doesn't exist even on lichess?
    # TODO: there is a problem with HTTP Error 404/502


def download_games(name,
                   input_format,
                   file_name='resources/game_ids.dat'
                   ):
    token = setup()
    get_game_ids(name)

    with open(file_name, 'r') as f:
        game_id_list = f.readlines()
    game_id_list = [(game_id_list[0][i:i + 8]) for i in
                    range(0, len(game_id_list[0]), 8)]

    for id in game_id_list:
        game, filename = get_game_filename(id,
                                           token,
                                           input_format)

        # what was I using these for?


if __name__ == "__main__":
    download_games('carequinha', 'PGN')
