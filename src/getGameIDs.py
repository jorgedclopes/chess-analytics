import os
import random
from dotenv import load_dotenv
from lichess.format import SINGLE_PGN, PGN
import lichess.api
from pprint import pprint
from src.setup import setup

def getGameIDs(name):

    pathName = 'game_ids.dat'
    if(os.path.exists(pathName)):
        return

    user = lichess.api.user(name)

    TOKEN = setup()
    #pprint(TOKEN)

    #print(user['perfs'].values())
    #for i in user['perfs']:
    #    print(i, "\t", user['perfs'][i])

    #time in miliseconds since Jan 1st 1970
    len_blitz_games = user['perfs']['blitz']['games']
    initial_time = user['createdAt']
    latest_time = user['seenAt']
    delta_time = latest_time-initial_time

    print(initial_time,latest_time, delta_time)

    games_list = list()

    increment = int(delta_time/100)
    for time in range(initial_time,latest_time,increment):
        games_generator = lichess.api.user_games(
                    name,perfType='blitz',
                    since=time, until=time+increment,auth=TOKEN)

        games_list += list(games_generator)
        game_len = len(games_list)
        print("{:15d} {:06.2f} {:4d} {:5d}".format(time, (time-initial_time)/delta_time*100, game_len, len_blitz_games))


    #for game in games_list:
#    print(game['id'])

    with open(pathName,'w') as f:
        for game in games_list:
            f.writelines(game['id'])
#print(type(games))
#games_length = sum(1 for _ in games)

if __name__ == "__main__":
    getGameIDs('carequinha')
