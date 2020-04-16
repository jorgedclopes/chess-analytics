import pgn
import sys
import os

def divide_by_tag(game_list, tag_name):
    games_by_tag = {}

    for game in game_list:
        tag = getattr(game, tag_name)
        if tag in games_by_tag:
            games_by_tag[tag].append(game)
        else:
            games_by_tag[tag] = [game]

    return games_by_tag


def list_tags(games_by_tag):
    max_width = max([len(tag) for tag in games_by_tag])

    for tag in games_by_tag:
        print('{0:{padding}{align}{width!s}}{1!s}'.format(
            tag, len(games_by_tag[tag]),
            padding=' ', align='<', width=max_width+2))


def divide_by_result(game_list, username='DRNbw'):
    results = {'win': [], 'loss': [], 'draw': []}

    for game in game_list:
        if game.white == username:
            is_white = True
        elif game.black == username:
            is_white = False
        else:
            print(game)
            continue

        if game.result == '1/2-1/2':
            result = 'draw'
        elif game.result == '1-0':
            if is_white:
                result = 'win'
            else:
                result = 'loss'
        elif game.result == '0-1':
            if not is_white:
                result = 'win'
            else:
                result = 'loss'
        else:
            print(game)
            continue

        results[result].append(game)

    return results


#pgn_file = 'lichess_DRNbw_2016-12-14.pgn'
# pgn_file = sys.argv[-1]
#
# pgn_text = open(pgn_file).read()
# pgn_game = pgn.PGNGame()
#games = pgn.loads(pgn_text)
games = []
folder = sys.argv[-1]
for filename in os.listdir(folder):
    with open(folder+"/"+filename) as f:
        pgnGame = pgn.loads(f.read())[0]
        games.append(pgnGame)

#print(games)

list_tags(divide_by_tag(games, 'result'))

# Required Tags: “Event”, “Site”, “Date”,
#                “Round”, “White”, “Black”, “Result”
# Optional Tags: “Annotator”, “PlyCount”,
#                “TimeControl”, “Time”, “Termination”,
#                “Mode”, “FEN”
# Extra Tags: 'Variant', 'Opening', 'WhiteElo', 'BlackElo'

# standard_games = [game for game in games
#                   if game.variant == 'Standard']

games_by_variant = divide_by_tag(games, 'variant')

standard_games = games_by_variant['Standard']

games_by_time = divide_by_tag(standard_games, 'timecontrol')
try:
    games_by_time.pop('-')
except KeyError:
    pass

print('')
print('Time (s) | Tot    | Win%   | W      | D      | L      ')
print('---------+--------+--------+--------+--------+--------')

times_increasing = sorted(games_by_time.keys(),
                          key=lambda time: eval(time))
times_by_played = sorted(games_by_time.keys(),
                         key=lambda time: len(games_by_time[time]),
                         reverse=True)

for time in times_by_played:
    results = divide_by_result(games_by_time[time],
                               'carequinha')

    num_wins = len(results['win'])
    num_draws = len(results['draw'])
    num_losses = len(results['loss'])
    num_total = num_wins + num_draws + num_losses

    if num_total > 0:
        win_rate = num_wins / num_total
    else:
        win_rate = -1

    print('{:8} | {:<{width}} | {:6.2f} | {:<{width}} | {:<{width}} | {:<{width}}'.format(
        time,
        num_total,
        100 * win_rate,
        num_wins,
        num_draws,
        num_losses,
        width='6'))

print('\nDone')