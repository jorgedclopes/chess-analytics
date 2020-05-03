import pgn
import json


class ChessPlayer():
    def __init__(self, name, rating=None):
        self.name = name

        self.rating = 0
        if rating is not None:
            self.rating = rating


class ChessGame():
    def __init__(self):
        self.rated = None
        self.variant = None
        self.speed = None
        self.status = None
        self.site = None
        self.date = None

        # TODO generic number of players? (4 player chess on chess.com...)
        self.white = None
        self.black = None

        self.winner = None

        # TODO time control as string or
        self.timecontrol = None

    def __str__(self):
        return f'{"Rated" if self.rated else "Unrated"} {self.variant} {self.speed}'

    @staticmethod
    def load_from_pgn_game(pgn_string):
        return pgn.loads(pgn_string)

    @staticmethod
    def load_from_json(json_dict, source='lichess'):
        new_game = ChessGame()

        for attr in ['rated', 'variant', 'speed', 'status']:
            setattr(new_game, attr, json_dict[attr])

        if source == 'lichess':
            new_game.site = f'https://lichess.org/{json_dict["id"]}'

        # new_game.site = site
        # new_game.date = date
        # new_game.round = round
        # new_game.white = white
        # new_game.black = black
        # new_game.result = result
        # new_game.annotator = None
        # new_game.plycount = None
        # new_game.timecontrol = None
        # new_game.time = None
        # new_game.termination = None
        # new_game.mode = None
        # new_game.fen = None

        # new_game.moves = []

        return new_game
