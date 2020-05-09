# chess.com API -> https://www.chess.com/news/view/published-data-api
# The API has been used to download monthly archives for a user using a Python3 program.
# This program works as of 5/05/2020


import urllib
import urllib.request
import glob, os

username = "mythaar" #change
path_to_directory = "/Users/student/Desktop/pgn_downloads/" #change -> where the files will be downloaded
new_file_name = 'all_games.pgn' #change
baseUrl = "https://api.chess.com/pub/player/" + username + "/games/"
archivesUrl = baseUrl + "archives"

#read the archives url and store in a list

f = urllib.request.urlopen(archivesUrl)
archives = f.read().decode("utf-8")
archives = archives.replace("{\"archives\":[\"", "\",\"")
archivesList = archives.split("\",\"" + baseUrl)
archivesList[len(archivesList)-1] = archivesList[len(archivesList)-1].rstrip("\"]}")

#download all the archives
for i in range(len(archivesList)-1):
    url = baseUrl + archivesList[i+1] + "/pgn"
    filename = archivesList[i+1].replace("/", "-")
    urllib.request.urlretrieve(url, path_to_directory + filename + ".pgn") #change


os.chdir(path_to_directory)


filenames = []
for file in glob.glob("*.pgn"):
    filenames.append(file)
with open(path_to_directory+new_file_name, 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())
