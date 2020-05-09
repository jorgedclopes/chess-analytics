# chess.com API -> https://www.chess.com/news/view/published-data-api
# The API has been used to download monthly archives for a user using a Python3 program.
# This program works as of 5/05/2020


import glob
import os
import urllib.request
from ast import literal_eval
from pathlib import Path


def get_chess_dot_com_games(
    username: str = "mythaar",
    path: str = "resources/chessdotcom_pgn_downloads/",
    new_file_name: str = 'all_games.pgn'
):
    Path(path).mkdir(parents=True,
                     exist_ok=True)
    base_url = "https://api.chess.com/pub/player/" + \
               username + \
               "/games/"
    archives_url = base_url + "archives"

    # read the archives url and store in a list

    f = urllib.request.urlopen(archives_url)
    read_f = f.read().decode("utf-8")
    archives_list = list(
        map(lambda x: x.split('games/')[-1],
            list(literal_eval(read_f).values())[0]))

    # pprint("archives")
    # pprint(literal_eval(read_f).values())
    # pprint(list(literal_eval(read_f).values())[0])
    # pprint(archives_list)

    # download all the archives
    for archive in archives_list:
        url = base_url + archive + "/pgn"
        filename = archive.replace("/", "-")
        urllib.request\
              .urlretrieve(url,
                           path + filename + ".pgn")

    with open(path + new_file_name, 'w') as outfile:
        for fname in glob.glob(path + "20*.pgn"):
            with open(fname) as infile:
                outfile.write(infile.read())
            os.remove(fname)


if __name__ == '__main__':  # pragma: no cover
    get_chess_dot_com_games()
