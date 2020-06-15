import os
import shutil
import warnings

import lichess.api
import pytest

from src.load_games import load_games
from src.get_games_lichess import download_games

# this is not ideal but it works for now
TIME_30MIN = 30 * 60 * 1000


class TestReadFile:

    def test_from_temp_folder(self):
        assert True
