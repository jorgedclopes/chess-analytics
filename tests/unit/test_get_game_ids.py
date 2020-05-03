import logging
import os
import shutil

import lichess
from src.get_games import download_games

# this is not ideal but it works for now
TIME_30MIN = 30 * 60 * 1000


class Test:

    def test_no_game_ids(self):
        log = logging.getLogger('test_no_game_ids')
        path = 'resources/game_ids_test.dat'
        if os.path.exists(path):
            os.remove(path)
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        log.debug('before function call')
        output = download_games(name='carequinha',
                                path_name=path,
                                initial_time=initial_time,
                                latest_time=initial_time +
                                            TIME_30MIN,
                                is_rated=None)
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
        output = download_games(name='carequinha',
                                path_name=path,
                                pref_type='blitz',
                                initial_time=initial_time,
                                latest_time=initial_time +
                                            TIME_30MIN,
                                is_rated=None)
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
        log.debug('before function call')
        output = download_games(name='carequinha',
                                path_name=path,
                                initial_time=initial_time,
                                latest_time=initial_time +
                                            TIME_30MIN,
                                is_rated=None)
        log.debug('after function call')
        assert output == "From remote."
        output = download_games(name='carequinha',
                                path_name=path,
                                initial_time=initial_time,
                                latest_time=initial_time +
                                            TIME_30MIN,
                                is_rated=None)
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

    def test_initial_time_default_arguments(self):
        log = logging.getLogger('test_no_game_ids')
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        path = 'resources/game_ids_test.dat'

        log.debug('before function call')
        db_test_dir1 = 'resources/PGN_database_test1'
        output1 = download_games(name='carequinha',
                                 path_name=path,
                                 db_dir=db_test_dir1,
                                 initial_time=initial_time,
                                 latest_time=initial_time +
                                             TIME_30MIN,
                                 is_rated=None)
        os.remove('resources/game_ids_test.dat')

        db_test_dir2 = 'resources/PGN_database_test2'
        output2 = download_games(name='carequinha',
                                 path_name=path,
                                 db_dir=db_test_dir2,
                                 latest_time=initial_time +
                                             TIME_30MIN,
                                 is_rated=None)
        os.remove('resources/game_ids_test.dat')
        log.debug('after function call')

        expected = os.listdir(db_test_dir1)
        actual = os.listdir(db_test_dir2)
        shutil.rmtree(db_test_dir1)
        shutil.rmtree(db_test_dir2)
        assert expected == actual

    def test_latest_time_default_arguments(self):
        log = logging.getLogger('test_no_game_ids')
        user = lichess.api.user('carequinha')
        latest_time = user['seenAt']
        path = 'resources/game_ids_test.dat'

        log.debug('before function call')
        db_test_dir1 = 'resources/PGN_database_test1'
        output1 = download_games(name='carequinha',
                                 path_name=path,
                                 db_dir=db_test_dir1,
                                 initial_time=latest_time -
                                             TIME_30MIN,
                                 latest_time=latest_time,
                                 is_rated=None)
        os.remove('resources/game_ids_test.dat')

        db_test_dir2 = 'resources/PGN_database_test2'
        output2 = download_games(name='carequinha',
                                 path_name=path,
                                 db_dir=db_test_dir2,
                                 initial_time=latest_time -
                                             TIME_30MIN,
                                 is_rated=None)
        os.remove('resources/game_ids_test.dat')
        log.debug('after function call')

        expected = os.listdir(db_test_dir1)
        actual = os.listdir(db_test_dir2)
        shutil.rmtree(db_test_dir1)
        shutil.rmtree(db_test_dir2)
        assert expected == actual
