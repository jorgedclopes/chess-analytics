import numpy as np
from src.chess_utils.game_etl import array_reshape


class TestGameEtl:
    @staticmethod
    def test_game_finds_basic_attributes():
        data = np.array(['a', 'b', 'c', 'd', 'e', 'f'])
        actual = array_reshape(data, 2)
        expected = np.array([['a', 'b'], ['c', 'd'], ['e', 'f']])
        assert (expected == actual).all()

        actual = array_reshape(data, 3)
        expected = np.array([['a', 'b', 'c'], ['d', 'e', 'f']])
        assert (expected == actual).all()
