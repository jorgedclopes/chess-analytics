from src.get_games import get_games
import lichess
import logging
import os


class Test:
    def test_no_game_ids(self):
        log = logging.getLogger('test_no_game_ids')
        path = 'resources/game_ids_test.dat'
        if os.path.exists(path):
            os.remove(path)
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        log.warning('before function call')
        output = get_games(name='carequinha',
                           path_name=path,
                           initial_time=initial_time,
                           latest_time=initial_time +
                                       30 * 60 * 1000)
        log.debug('after function call')
        # check the first 30 minutes
        assert output == "From remote."
        with open(path, 'r') as f:
            game_id_list = f.readlines()
        game_id_list = [(game_id_list[0][i:i + 8]) for i in
                        range(0, len(game_id_list[0]), 8)]
        os.remove(path)
        assert len(game_id_list) == 2

    def test_no_game_ids_with_particular_pref_type(self):
        log = logging.getLogger('test_no_game_ids')
        path = 'resources/game_ids_test.dat'
        if os.path.exists(path):
            os.remove(path)
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        log.warning('before function call')
        output = get_games(name='carequinha',
                           path_name=path,
                           pref_type='blitz',
                           initial_time=initial_time,
                           latest_time=initial_time +
                                       30 * 60 * 1000)
        log.debug('after function call')
        # check the first 30 minutes
        assert output == "From remote."
        with open(path, 'r') as f:
            game_id_list = f.readlines()
        game_id_list = [(game_id_list[0][i:i + 8]) for i in
                        range(0, len(game_id_list[0]), 8)]
        os.remove(path)
        assert len(game_id_list) == 1

    def test_with_game_ids_with_particular_pref_type(self):
        log = logging.getLogger('test_no_game_ids')
        path = 'resources/game_ids_test.dat'
        if os.path.exists(path):
            os.remove(path)
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        log.warning('before function call')
        output = get_games(name='carequinha',
                           path_name=path,
                           initial_time=initial_time,
                           latest_time=initial_time +
                                       30 * 60 * 1000)
        log.debug('after function call')
        assert output == "From remote."
        output = get_games(name='carequinha',
                           path_name=path,
                           initial_time=initial_time,
                           latest_time=initial_time +
                                       30 * 60 * 1000)
        assert output == "Specifications ignored. " \
                         "Reading from file."
        with open(path, 'r') as f:
            game_id_list = f.readlines()
        game_id_list = [(game_id_list[0][i:i + 8]) for i in
                        range(0, len(game_id_list[0]), 8)]
        print(game_id_list)
        assert len(game_id_list) == 2
        assert game_id_list == ['OwUkcBo7', 'urC8tV4n']
        os.remove(path)
