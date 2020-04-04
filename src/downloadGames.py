import os
from dotenv import load_dotenv
from lichess.format import SINGLE_PGN, PGN, JSON
import lichess.api
from pprint import pprint
from src.setup import setup
from getGameIDs import getGameIDs
import sys


def getGameFilename(id, TOKEN, format):
    if format == 'JSON':
        format = JSON
        filename = 'JSON_database/'+id+'.json'
    elif format == 'PGN':
        format = PGN
        filename = 'PGN_database/'+id+'.pgn'
    else:
        raise NameError('No valid format.')


    if(not os.path.exists(filename)):
        game = lichess.api.game(id, format = format, auth=TOKEN)
        print("File " + filename + " does not exist yet. Downloading...")
        with open(filename,'w') as file:
            file.write(str(game))
    else:
        print("File " + filename + " already exists. Not overwritten.")
        with open(filename,'r') as file:
            game = file.read()

    return game, filename


def downloadGames(name, format):
    TOKEN = setup()
    getGameIDs(name)

    with open('game_ids.dat','r') as f:
        game_id_list = f.readlines()
    game_id_list = [(game_id_list[0][i:i+8]) for i in range(0,len(game_id_list[0]),8)]

    for id in game_id_list:
        game, filename = getGameFilename(id, TOKEN, format)

if __name__ == "__main__":
    downloadGames('carequinha','PGN')
