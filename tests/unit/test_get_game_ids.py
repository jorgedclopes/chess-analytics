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
    def test_no_game_ids_with_particular_pref_type(self):
        log = logging.getLogger('test_no_game_ids')
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        final_time = initial_time + TIME_30MIN
        db_test_dir = 'resources/PGN_database_test'
        log.debug('before function call')
        download_games(name='carequinha',
                       db_dir=db_test_dir,
                       perf_type='blitz',
                       time_period=[initial_time, final_time])
        game_id_list = os.listdir(db_test_dir)
        shutil.rmtree(db_test_dir)
        assert len(game_id_list) == 1

    def test_with_game_ids_with_particular_pref_type(self):
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        final_time = initial_time + TIME_30MIN
        db_test_dir = 'resources/PGN_database_test'
        # download_games(name='carequinha', db_dir=db_test_dir)
        with pytest.warns(ResourceWarning) as w:
            download_games(name='carequinha',
                           db_dir=db_test_dir,
                           time_period=[initial_time, final_time])
            warnings.warn('PGN database already downloaded.',
                          ResourceWarning)

        game_id_list = os.listdir(db_test_dir)
        shutil.rmtree(db_test_dir)
        assert len(w) == 1
        assert len(game_id_list) == 1
        assert game_id_list == ['carequinha.pgn']

    def test_initial_time_default_arguments(self):
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        final_time = initial_time + TIME_30MIN

        db_test_dir1 = 'resources/PGN_database_test1'
        download_games(name='carequinha',
                       db_dir=db_test_dir1,
                       time_period=[initial_time, final_time])

        db_test_dir2 = 'resources/PGN_database_test2'
        download_games(name='carequinha',
                       db_dir=db_test_dir2,
                       time_period=[initial_time, final_time])

        expected = os.listdir(db_test_dir1)
        actual = os.listdir(db_test_dir2)
        shutil.rmtree(db_test_dir1)
        shutil.rmtree(db_test_dir2)
        assert expected == actual

    def test_latest_time_default_arguments(self):
        log = logging.getLogger('test_no_game_ids')
        user = lichess.api.user('carequinha')
        final_time = user['seenAt']
        initial_time = final_time - TIME_30MIN

        log.debug('before function call')
        db_test_dir1 = 'resources/PGN_database_test1'
        download_games(name='carequinha',
                       db_dir=db_test_dir1,
                       time_period=[initial_time, final_time])

        db_test_dir2 = 'resources/PGN_database_test2'
        download_games(name='carequinha',
                       db_dir=db_test_dir2,
                       time_period=[initial_time, final_time])
        log.debug('after function call')

        expected = os.listdir(db_test_dir1)
        actual = os.listdir(db_test_dir2)
        shutil.rmtree(db_test_dir1)
        shutil.rmtree(db_test_dir2)
        assert expected == actual
