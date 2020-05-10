"""
  This file has the function to fetch token from .env file.

  To use this function one should import the library and
  call the function.
"""
import os
import warnings
from dotenv import load_dotenv


def setup(path: str = None,
          env_var: str = 'lichess_token',
          db_dir: str = 'resources/PGN_database'):
    """
    Function to fetch token from .env file.

    Parameters
    ----------
        path : str
            Path to .env file with lichess token.
        env_var : str
            Name of the variable to import.
        db_dir : str
            Setup and make folder if it does not already exist.

    Returns
    -------
        String
            Token from lichess account to connect to API.

    """

    if not os.path.isdir(db_dir):
        os.makedirs(db_dir)
    if path is not None:
        path = os.path.join(path, '.env')
    os.environ.clear()
    load_dotenv(dotenv_path=path, verbose=True)
    token = os.getenv(env_var)
    if token is None:
        warnings.warn("No token loaded.", ResourceWarning)
    return token
