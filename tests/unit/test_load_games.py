import os
import shutil
import warnings

import lichess.api
import pytest

from src.load_games import load_games
from src.get_games import download_games

# this is not ideal but it works for now
TIME_30MIN = 30 * 60 * 1000


class TestReadFile:

    def test_from_temp_folder(self):
        user = lichess.api.user('carequinha')
        initial_time = user['createdAt']
        final_time = initial_time + TIME_30MIN
        db_test_dir = 'resources/PGN_database_test_load_games'
        download_games(name='carequinha',
                       db_dir=db_test_dir,
                       pref_type='blitz',
                       latest_time=final_time)

        games = load_games(path=db_test_dir,
                           is_rated=True)
        # check the first 30 minutes
        shutil.rmtree(db_test_dir)
        assert len(games) == 1

    def test_temp_folder_with_no_games(self):
        db_test_dir = 'resources/PGN_database_test'
        os.mkdir(db_test_dir)
        with pytest.warns(ResourceWarning) as w:
            games = load_games(path=db_test_dir)
            warnings.warn("No games found in this folder.",
                          ResourceWarning)
        # check the first 30 minutes
        shutil.rmtree(db_test_dir)
        assert len(games) == 0
        assert len(w) == 2
