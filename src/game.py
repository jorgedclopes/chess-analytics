import pgn


class ChessPlayer:
    def __init__(self, name, rating=None):
        self.name = name

        self.rating = 0
        if rating is not None:
            self.rating = rating

    def __str__(self):
        return f'{self.name} ({self.rating})'


class ChessGame:
    def __init__(self):
        # General Game Information
        self.site = None
        self.date = None
        self.time = None
        # self.rated = None     ## PGN does not have this information
        self.variant = None
        # self.speed = None     ## PGN does not have this information
        self.timecontrol = None
        self.termination = None

        # Players, see class ChessPlayer
        self.players = {}
        self.result = None

        # Moves
        self.moves = None
        self.ply = 0
        self.turns = 0
        self.eco = None

        # Extra Info
        # self.stage_at_end = None      ## Ended at opening/midgame/endgame?

    def __str__(self):
        return (
            f'{self.variant} game between '
            f'{self.players["white"]} and {self.players["black"]}.\n'
            f'This game\'s time control was {self.timecontrol} was played in {self.date}. '
            f'The result was {self.result}.\n'
            f'The oppening code is {self.eco} and the game had a length of {self.turns} moves.'
        )

    @staticmethod
    def load_pgn_file(filepath):
        with open(filepath, 'r') as f:
            games = ChessGame.load_all_from_pgn(f.read())

        return games

    @staticmethod
    def load_all_from_pgn(pgn_string):
        games = [
            ChessGame.load_from_pgn_game(pgn_game)
            for pgn_game in pgn.loads(pgn_string)
        ]

        return games

    @staticmethod
    def load_from_pgn_game(pgn_game):
        """
        Game class from library attributes:
            'event', 'site', 'date', 'round', 'white', 'black',
            'result', 'annotator', 'plycount', 'timecontrol', 'time',
            'termination', 'mode', 'fen', 'moves', 'utcdate', 'utctime',
            'whiteelo', 'blackelo', 'whiteratingdiff', 'blackratingdiff',
            'variant', 'eco'
        """

        new_game = ChessGame()

        common_attributes = [
            'site', 'date', 'variant', 'timecontrol', 'termination',
            'eco', 'moves', 'result', 'utctime'
        ]
        for attr in common_attributes:
            new_game.__setattr__(attr, pgn_game.__getattribute__(attr))

        # Last move is the result
        new_game.moves.pop()

        # Players, see class ChessPlayer
        new_game.players = {
            'white': ChessPlayer(pgn_game.white, pgn_game.whiteelo),
            'black': ChessPlayer(pgn_game.black, pgn_game.blackelo),
        }

        # Moves
        new_game.ply = len(new_game.moves)
        new_game.turns = (new_game.ply + 1) // 2

        return new_game

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

    def get_result(self):
        result = ""
        if ((self.players['white'].name == "carequinha" and self.result == "1-0") or
                (self.players['black'].name == "carequinha" and self.result == "0-1")):
            result = "WIN"
        elif ((self.players['white'].name == "carequinha" and self.result == "0-1") or
                (self.players['black'].name == "carequinha" and self.result == "1-0")):
            result = "LOSS"
        elif self.result == "1/2-1/2":
            result = "DRAW"

        if result is None:
            raise RuntimeError("Get_result does not fall in any of the conditions.")
        return result
