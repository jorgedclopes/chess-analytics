import warnings

import pytest

from src.chess_utils.game import ChessGame, compute_delta_time


class TestGame:
    @staticmethod
    def test_game_finds_basic_attributes():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/loss_game_example.pgn")
        assert game is not None
        assert len(game) == 1
        for (k, v) in game[0].players.items():
            assert k in {"white", "black"}
            assert v.name in {"carequinha", "HardyJ"}
            assert v.rating in {1976, 1745}
        assert game[0].eco == "A43"

    @staticmethod
    def test_import_game_with_non_standard_format():
        with pytest.warns(Warning) as w:
            with pytest.raises(AttributeError) as e:
                ChessGame.load_pgn_file("tests/unit/pgn_files/bad_file.pgn")
        assert e.type is AttributeError
        assert len(w) > 0
        for wa in w:
            assert "'PGNGame' object has no attribute" in wa.message.args[0]

    @staticmethod
    def test_delta_time_computation_one_second():
        time = "00:00:01"
        expected = 1
        actual = compute_delta_time(time)
        assert actual == expected

    @staticmethod
    def test_delta_time_computation_one_minute():
        time = "00:01:00"
        expected = 60
        actual = compute_delta_time(time)
        assert actual == expected

    @staticmethod
    def test_delta_time_computation_one_hour():
        time = "01:00:00"
        expected = 3600
        actual = compute_delta_time(time)
        assert actual == expected

    @staticmethod
    def test_check_loss_result():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/loss_game_example.pgn")
        assert game[0].get_result('carequinha') == 'LOSS'

    @staticmethod
    def test_check_win_result():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        assert game[0].get_result('carequinha') == 'WIN'

    @staticmethod
    def test_check_draw_result():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/draw_game_example.pgn")
        assert game[0].get_result('carequinha') == 'DRAW'

    @staticmethod
    def test_check_wrong_player():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        with pytest.warns(Warning) as w:
            game[0].get_result('abc')
            # warnings.warn("No token loaded.", Warning)
        assert len(w) == 1
        assert w[0].message.args[0] == "That player is not in this game"

    @staticmethod
    def test_black_rating_difference():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/draw_game_example.pgn")
        assert game[0].get_rating_diff('carequinha') == 1863 - 1950

    @staticmethod
    def test_white_rating_difference():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/loss_game_example.pgn")
        assert game[0].get_rating_diff('carequinha') == 1976 - 1745

    @staticmethod
    def test_get_player_names():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        for n in game[0].get_player_names():
            assert n in ('lorenzm', 'carequinha')

    '''
    Clocks are taken out when we import the game
    '''

    @staticmethod
    def test_split_times():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        # list of moves - in this case specific to the game
        expected_moves = ['d4', 'd5', 'c4', 'e6', 'Nc3', 'Nf6', 'cxd5', 'Nxd5', 'Nf3', 'Nxc3', 'bxc3', 'Be7', 'e4',
                          'b6', 'Bc4', 'Bb7', 'Qc2', 'Nd7', 'O-O', 'c5', 'd5', 'exd5', 'exd5', 'O-O', 'Re1', 'Nf6',
                          'Rd1', 'Qd6', 'Bb3', 'Rfd8', 'c4', 'a6', 'Qf5', 'b5', 'cxb5', 'axb5', 'Bf4', 'Qd7', 'Qxd7',
                          'Rxd7', 'd6', 'Bf8', 'Ne5', 'Rdd8', 'Nxf7', 'c4', 'Nxd8', 'Rxd8', 'Bc2', 'Ne8', 'd7', 'Nf6',
                          'Bc7', 'Rxd7', 'Rxd7', 'Nxd7', 'Bf5', 'Nf6', 'Be6+', 'Kh8', 'Rb1', 'Bc6', 'Rd1', 'Be7', 'Ba5',
                          'h6', 'Bf5', 'Kg8', 'Bg6', 'Nd5', 'Re1', 'Bf6', 'Re6', 'Ne7', 'Bb4', 'Bd5', 'Rd6', 'Be5',
                          'Rd8#']
        # list of numbers - in this case specific to the game
        expected_clocks = [180.0, 180.0, 180.0, 180.0, 180.0, 179.0, 180.0, 178.0, 178.0, 177.0, 178.0, 177.0, 177.0,
                           177.0, 175.0, 177.0, 173.0, 175.0, 172.0, 175.0, 169.0, 174.0, 169.0, 173.0, 168.0, 172.0,
                           161.0, 161.0, 160.0, 160.0, 160.0, 154.0, 158.0, 153.0, 157.0, 152.0, 155.0, 150.0, 153.0,
                           149.0, 147.0, 147.0, 143.0, 144.0, 140.0, 135.0, 139.0, 134.0, 135.0, 132.0, 132.0, 131.0,
                           131.0, 129.0, 130.0, 129.0, 126.0, 126.0, 124.0, 124.0, 122.0, 123.0, 118.0, 120.0, 116.0,
                           118.0, 112.0, 116.0, 111.0, 112.0, 108.0, 109.0, 106.0, 98.0, 103.0, 92.0, 99.0, 90.0, 97.0]
        assert game[0].moves == expected_moves
        assert game[0].clocks == expected_clocks

    @staticmethod
    def test_get_player_names_white():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        assert game[0].get_player_color('carequinha') == 'white'

    @staticmethod
    def test_get_player_names_black():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/draw_game_example.pgn")
        assert game[0].get_player_color('carequinha') == 'black'

    @staticmethod
    def test_get_player_no_user():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        with pytest.raises(UserWarning) as e:
            game[0].get_player_color('abc')
        assert e.typename == 'UserWarning'
        assert str(e.value.args[0]) == 'No such player in this game.'

    @staticmethod
    def test_get_opponent_colors():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        assert game[0].get_opponent_color('carequinha') == ['black']

    @staticmethod
    def test_get_player_rating():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        rating = game[0].get_player_rating('carequinha')
        assert type(rating) == int
        assert rating == 1912

# TODO make tests with users that are not in the games
