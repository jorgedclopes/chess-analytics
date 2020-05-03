import logging
import os
import shutil
import warnings

import lichess.api
import pytest

from src.get_games import download_games

# this is not ideal but it works for now
TIME_30MIN = 30 * 60 * 1000


class TestDownload:

    # def test_no_game_ids(self):
    #     log = logging.getLogger('test_no_game_ids')
    #     user = lichess.api.user('carequinha')
    #     initial_time = user['createdAt']
    #     final_time = initial_time + TIME_30MIN
    #     log.debug('before function call')
    #     output = download_games(name='carequinha',
    #                             initial_time=initial_time,
    #                             latest_time=final_time,
    #                             is_rated=None)
    #     log.debug('after function call')
    #     # check the first 30 minutes
    #     assert output == "From remote."
    #     game_id_list = os.listdir('resources/PGN_database')
    #     assert len(game_id_list) == 2

    def test_no_game_ids_with_particular_pref_type(self):
        log = logging.getLogger('test_no_game_ids')
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        final_time = initial_time + TIME_30MIN
        db_test_dir = 'resources/PGN_database_test'
        log.debug('before function call')
        download_games(name='carequinha',
                       db_dir=db_test_dir,
                       pref_type='blitz',
                       initial_time=initial_time,
                       latest_time=final_time,
                       is_rated=None)
        log.debug('after function call')

        # check the first 30 minutes
        game_id_list = os.listdir(db_test_dir)
        shutil.rmtree(db_test_dir)
        assert len(game_id_list) == 1

    def test_with_game_ids_with_particular_pref_type(self):
        log = logging.getLogger('test_no_game_ids')
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        final_time = initial_time + TIME_30MIN
        db_test_dir = 'resources/PGN_database_test'
        log.debug('before function call')
        download_games(name='carequinha',
                       db_dir=db_test_dir,
                       initial_time=initial_time,
                       latest_time=final_time,
                       is_rated=None)
        log.debug('after function call')
        with pytest.warns(ResourceWarning) as w:
            download_games(name='carequinha',
                           db_dir=db_test_dir,
                           initial_time=initial_time,
                           latest_time=final_time,
                           is_rated=None)
            warnings.warn('PGN database already downloaded.',
                          ResourceWarning)

        game_id_list = os.listdir(db_test_dir)
        shutil.rmtree(db_test_dir)
        assert len(w) == 2
        assert len(game_id_list) == 2
        assert game_id_list == ['OwUkcBo7.pgn', 'urC8tV4n.pgn']

    def test_initial_time_default_arguments(self):
        log = logging.getLogger('test_no_game_ids')
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        final_time = initial_time + TIME_30MIN

        log.debug('before function call')
        db_test_dir1 = 'resources/PGN_database_test1'
        download_games(name='carequinha',
                       db_dir=db_test_dir1,
                       initial_time=initial_time,
                       latest_time=final_time,
                       is_rated=None)

        db_test_dir2 = 'resources/PGN_database_test2'
        download_games(name='carequinha',
                       db_dir=db_test_dir2,
                       latest_time=initial_time + TIME_30MIN,
                       is_rated=None)
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
        initial_time = latest_time - TIME_30MIN

        log.debug('before function call')
        db_test_dir1 = 'resources/PGN_database_test1'
        download_games(name='carequinha',
                       db_dir=db_test_dir1,
                       initial_time=initial_time,
                       latest_time=latest_time,
                       is_rated=None)

        db_test_dir2 = 'resources/PGN_database_test2'
        download_games(name='carequinha',
                       db_dir=db_test_dir2,
                       initial_time=initial_time,
                       is_rated=None)
        log.debug('after function call')

        expected = os.listdir(db_test_dir1)
        actual = os.listdir(db_test_dir2)
        shutil.rmtree(db_test_dir1)
        shutil.rmtree(db_test_dir2)
        assert expected == actual
