import warnings

import pytest

from src.setup_env import setup


class TestSetup:
    def test_there_is_no_dotenv(self):
        with pytest.warns(Warning) as w:
            token = setup('/this_not_real_path')
            warnings.warn("No token loaded.", Warning)
        assert token is None
        assert len(w) == 2

    def test_there_is_a_dotenv(self):
        token = setup(path='resources/')
        assert isinstance(token, str)
        # checks if the string is not empty
        assert token is not False

    def test_no_dir(self):
        temp_dir = 'resources/temp_test_dir/'
        with pytest.warns(Warning) as w:
            token = setup(path=temp_dir)
            warnings.warn("No token loaded.", Warning)
        assert token is None
        assert len(w) == 2
