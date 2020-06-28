import warnings
import pytest
from src.setup_env import setup


class TestSetup:
    def test_there_is_no_dotenv(self):
        with pytest.warns(ResourceWarning) as w:
            token = setup('/this_not_real_path')
            warnings.warn("No token loaded.", ResourceWarning)
        assert token is None
        assert len(w) == 2

    def test_there_is_a_dotenv(self):
        token = setup(path='resources/')
        assert isinstance(token, str)
        # checks if the string is not empty
        assert token is True
