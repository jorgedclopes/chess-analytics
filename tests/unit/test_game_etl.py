import numpy as np

from src.chess_utils.game import ChessGame
from src.chess_utils.game_etl import array_reshape, get_result_list, data_transform_array


class TestGameEtl:
    def test_game_finds_basic_attributes(self):
        data = np.array(['a', 'b', 'c', 'd', 'e', 'f'])
        actual = array_reshape(data, 2)
        expected = np.array([['a', 'b'], ['c', 'd'], ['e', 'f']])
        assert (expected == actual).all()

        actual = array_reshape(data, 3)
        expected = np.array([['a', 'b', 'c'], ['d', 'e', 'f']])
        assert (expected == actual).all()

    def test_result_list(self):
        games = ChessGame.load_pgn_file("tests/unit/pgn_files/two_games_example.pgn")
        actual = get_result_list(games, 'carequinha')
        expected_data = {'LOSS': 1, 'WIN': 1}
        expected = (np.array(list(expected_data.keys()), dtype='<U4'),
                    np.array(list(expected_data.values())))
        # values and keys are separated into 2 np.arrays
        for x, y in zip(expected, actual):
            assert (x == y).all()

    def test_data_transform_array(self):
        data = [1, 2, 3]
        funcs = [lambda x: x ** 2, lambda x: 2 * x]

        # why parenthesis work and square brackets don't?
        expected_data = [(1, 2), (4, 4), (9, 6)]
        expected = np.array(expected_data, dtype=[('X', '<i8'), ('Y', '<i8')])
        actual = data_transform_array(data, funcs)
        assert (expected == actual).all()
