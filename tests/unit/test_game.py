from chess_utils.game import ChessGame


class TestGame:
    @staticmethod
    def test_some_test():
        game = ChessGame.load_pgn_file("tests/unit/example.pgn")
        assert game is not None
        assert len(game) == 1
        for (k, v) in game[0].players.items():
            assert k in {"white", "black"}
            assert v.name in {"carequinha", "HardyJ"}
            assert v.rating in {"1976", "1745"}
        assert game[0].eco == "A43"
