import os
from lichess.format import SINGLE_PGN, PGN, JSON
import lichess.api
from pprint import pprint
from setup import setup
from getGameIDs import get_game_ids
import sys


def get_game_filename(file_id, token, input_format):
    if input_format == 'JSON':
        input_format = JSON
        filename = 'resources/JSON_database/' + file_id + '.json'
    elif input_format == 'PGN':
        input_format = PGN
        filename = 'resources/PGN_database/' + file_id + '.pgn'
    else:
        raise NameError('No valid format.')

    if not os.path.exists(filename):
        game = lichess.api.game(file_id, format=input_format, auth=token)
        print("File " + filename + " does not exist yet. Downloading...")
        with open(filename, 'w') as file:
            file.write(str(game))
    else:
        print("File " + filename + " already exists. Not overwritten.")
        with open(filename, 'r') as file:
            game = file.read()

    return game, filename
    # what if file doesn't exist?


def download_games(name, input_format):
    token = setup()
    get_game_ids(name)

    with open('resources/game_ids.dat', 'r') as f:
        game_id_list = f.readlines()
    game_id_list = [(game_id_list[0][i:i + 8]) for i in range(0, len(game_id_list[0]), 8)]

    for id in game_id_list:
        game, filename = get_game_filename(id, token, input_format)
        # what was I using these for?


if __name__ == "__main__":
    download_games('carequinha', 'PGN')
