import pytest
from src.chess_utils.game import ChessGame, compute_delta_time


class TestGame:
    @staticmethod
    def test_game_finds_basic_attributes():
        game = ChessGame.load_pgn_file("tests/unit/pgn_files/example.pgn")
        assert game is not None
        assert len(game) == 1
        for (k, v) in game[0].players.items():
            assert k in {"white", "black"}
            assert v.name in {"carequinha", "HardyJ"}
            assert v.rating in {"1976", "1745"}
        assert game[0].eco == "A43"

    @staticmethod
    @pytest.mark.filterwarnings("ignore")
    def test_import_game_with_non_standard_format():
        with pytest.raises(AttributeError) as e:
            ChessGame.load_pgn_file("tests/unit/pgn_files/bad_file.pgn")
        assert e.type is AttributeError

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
