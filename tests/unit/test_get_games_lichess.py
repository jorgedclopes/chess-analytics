import logging
import os
import shutil
import warnings

import lichess.api
import pytest

from src.get_games_lichess import download_games

# this is not ideal but it works for now
TIME_30MIN = 30 * 60 * 1000


class TestDownload:
    def test_no_game_ids_with_particular_pref_type(self):
        log = logging.getLogger('test_no_game_ids')
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        final_time = initial_time + TIME_30MIN
        os.mkdir('tests/resources')
        db_test = 'tests/resources/PGN_database_test.pgn'
        log.debug('before function call')
        download_games(name='carequinha',
                       dest_file=db_test,
                       pref_type='blitz',
                       latest_time=final_time)
        game_id_list = os.path.exists(db_test)
        shutil.rmtree('tests/resources')
        assert game_id_list

    def test_with_game_ids_with_particular_pref_type(self):
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        final_time = initial_time + TIME_30MIN
        os.mkdir('tests/resources')
        db_test = 'tests/resources/PGN_database_test.pgn'
        download_games(name='carequinha',
                       dest_file=db_test,
                       initial_time=initial_time,
                       latest_time=final_time)
        with pytest.warns(ResourceWarning):
            download_games(name='carequinha',
                           dest_file=db_test,
                           initial_time=initial_time,
                           latest_time=final_time)
            warnings.warn('PGN database already downloaded.',
                          ResourceWarning)

        game_id_list = os.path.exists(db_test)
        # expected = sorted(['OwUkcBo7.pgn', 'urC8tV4n.pgn'])
        shutil.rmtree('tests/resources')
        assert game_id_list

    def test_initial_time_default_arguments(self):
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        os.mkdir('tests/resources')
        final_time = initial_time + TIME_30MIN

        db_test_dir1 = 'tests/resources/PGN_database_test1.pgn'
        download_games(name='carequinha',
                       dest_file=db_test_dir1,
                       initial_time=initial_time,
                       latest_time=final_time)

        db_test_dir2 = 'tests/resources/PGN_database_test2.pgn'
        download_games(name='carequinha',
                       dest_file=db_test_dir2,
                       latest_time=initial_time + TIME_30MIN)

        game_id_list1 = os.path.exists(db_test_dir1)
        game_id_list2 = os.path.exists(db_test_dir2)
        shutil.rmtree('tests/resources')
        assert game_id_list1
        assert game_id_list2
