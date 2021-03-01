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
            ChessGame.load_pgn_file("tests/unit/pgn_files/bad_file.pgn")
        assert len(w) > 0
        for wa in w:
            assert "'PGNGame' object has no attribute" in wa.message.args[0]

    @staticmethod
    def test_delta_time_computation():
        time = "00:00:01"
        expected = 1
        actual = compute_delta_time(time)
        assert actual == expected

        time = "00:01:00"
        expected = 60
        actual = compute_delta_time(time)
        assert actual == expected

        time = "01:00:00"
        expected = 3600
        actual = compute_delta_time(time)
        assert actual == expected

    @staticmethod
    def test_check_result():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/loss_game_example.pgn")
        assert game[0].get_result('carequinha') == 'LOSS'

        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        assert game[0].get_result('carequinha') == 'WIN'

        game = ChessGame.load_pgn_file("tests/unit/pgn_files/draw_game_example.pgn")
        assert game[0].get_result('carequinha') == 'DRAW'

        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        with pytest.warns(Warning) as w:
            game[0].get_result('abc')
        assert len(w) == 1
        assert w[0].message.args[0] == "That player is not in this game"

    @staticmethod
    def test_rating_difference():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/draw_game_example.pgn")
        assert game[0].get_rating_diff('carequinha') == 1863 - 1950

        game = ChessGame.load_pgn_file("tests/unit/pgn_files/loss_game_example.pgn")
        assert game[0].get_rating_diff('carequinha') == 1976 - 1745

    @staticmethod
    def test_get_player_names():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        for n in game[0].get_player_names():
            assert n in ('lorenzm', 'carequinha')

    @staticmethod
    def test_get_player_colors():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        assert game[0].get_player_color('carequinha') == 'white'

        game = ChessGame.load_pgn_file("tests/unit/pgn_files/draw_game_example.pgn")
        assert game[0].get_player_color('carequinha') == 'black'

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
        assert isinstance(rating, int)
        assert rating == 1912

    @staticmethod
    def test_get_opponent_rating():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        rating = game[0].get_opponent_rating('carequinha')
        assert rating == [2020]

        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        with pytest.raises(UserWarning) as e:
            game[0].get_opponent_rating('abc')
        assert e.typename == 'UserWarning'
        assert str(e.value.args[0]) == 'No such player in this game.'

    @staticmethod
    def test_parse_month_years():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        time = game[0].parse_month_year()
        assert time == 2019.75
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/loss_game_example.pgn")
        time = game[0].parse_month_year()
        assert time == 2016

    @staticmethod
    def test_parse_hours():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/win_game_example.pgn")
        time = game[0].parse_hours()
        assert time == 12
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/loss_game_example.pgn")
        time = game[0].parse_hours()
        assert time == 15
