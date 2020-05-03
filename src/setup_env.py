"""
  This file has the function to fetch token from .env file.

  Unless you are developing, there is no point in
  calling this function.

  To use this function one should import the library and
  call the function.
"""
import os
import warnings
from dotenv import load_dotenv


def setup(path: str = None,
          env_var: str = 'lichess_token',
          db_dir: str = 'resources/PGN_database'):
    """Function to fetch token from .env file.

    Args:
        path (str): Path to .env file with lichess token.
        env_var (str): Name of the variable to import.
        db_dir (str): Setup and make folder if it doesn't
            already exist.

    Returns:
        token (str): Token from lichess account to connect
    to API.
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
