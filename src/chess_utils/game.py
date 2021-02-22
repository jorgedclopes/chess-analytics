import warnings
from datetime import timedelta
import numpy as np
import pgn


def compute_delta_time(time):
    time_args = ['hours', 'minutes', 'seconds']
    func_arg = {arg: int(val) for val, arg in zip(time.split(':'), time_args)}
    return timedelta(**func_arg).total_seconds()


class ChessPlayer:
    def __init__(self, name, rating=None):
        self.name = name

        self.rating = 0
        if rating is not None:
            self.rating = rating

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return False

    def __str__(self):
        return f'{self.name} ({self.rating})'


class ChessGame:
    def __init__(self):
        # General Game Information
        self.site = None
        self.date = None
        self.time = None
        self.utctime = None
        self.variant = None
        self.timecontrol = None
        self.termination = None

        # Players, see class ChessPlayer
        self.players = {}
        self.owner = None
        self.result = None

        # Moves
        self.moves = []
        self.clocks = None
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

    # This should also be a constructor of some sort
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
            try:
                new_game.__setattr__(attr, pgn_game.__getattribute__(attr))
            except AttributeError as e:
                warnings.warn(str(e))

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
        new_game.moves, new_game.clocks = new_game.split_moves_clocks()

        return new_game

    def is_player_or_color(self, user, color):
        return user in (self.players[color], color)

    def get_player_names(self):
        return (p.name for p in self.players.values())

    def get_result(self, user):
        result = ""
        if (user not in self.get_player_names()) and (user not in ("white", "black")):
            result = "Error - that player is not in this game."
            warnings.warn("That player is not in this game", Warning)
        elif ((self.is_player_or_color(user, 'white') and self.result == "1-0") or
              (self.is_player_or_color(user, 'black') and self.result == "0-1")):
            result = "WIN"
        elif ((self.is_player_or_color(user, 'white') and self.result == "0-1") or
              (self.is_player_or_color(user, 'black') and self.result == "1-0")):
            result = "LOSS"
        elif self.result == "1/2-1/2":
            result = "DRAW"

        if result is None:
            raise RuntimeError("Get_result does not fall in any of the conditions.")
        return result

    def get_rating_diff(self, user):
        if self.players['white'] == user:
            factor = 1
        else:
            factor = -1
        r = factor * (int(self.players['white'].rating) - int(self.players['black'].rating))
        return r

    def split_moves_clocks(self):
        if isinstance(self.moves, list) and len(self.moves) >= 2:
            if "clk" in self.moves[1]:
                moves = self.moves[::2]
                clocks_strings = [s[8:15] for s in self.moves[1::2]]
                clocks = [compute_delta_time(s)
                          for s in clocks_strings]
                return moves, clocks
        return self.moves, None

    def get_player_color(self, user):
        for k, v in self.players.items():
            if v == user:
                return k
        raise UserWarning('No such player in this game.')

    def get_opponent_color(self, user):
        player_color = self.get_player_color(user)
        opponent_colors = [x is not player_color for x in self.players]
        # opponent_color = 'black' if (player_color == 'white')
        # else 'white' if (player_color == 'black')
        # else None
        return opponent_colors

    def get_player_rating(self, user):
        color = self.get_player_color(user)
        return self.players[color].rating

    def get_opponent_rating(self, user):
        color = self.get_opponent_color(user)
        return self.players[color].rating

    def parse_month_year(self):
        year = self.date.split('.')[0]
        month = self.date.split('.')[1]
        return float(year) + float(month) / 12 - 1 / 12

    def parse_hours(self):
        return int(self.utctime.split(':')[0])

    def get_month_year(self):
        return np.datetime64(self.date.replace('.', '-'), 'M')
