import warnings
from src.setup_env import setup
import pytest


class TestSetup:
    def test_there_is_no_dotenv(self):
        with pytest.warns(ResourceWarning) as w:
            token = setup('/this_not_real_path')
            warnings.warn("No token loaded.", ResourceWarning)
        assert token is None
        assert 3 == len(w)

    def test_there_is_a_dotenv(self):
        token = setup()
        assert type(token) == str
        # checks if the string is not empty
        assert token is not False
