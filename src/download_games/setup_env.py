"""
  This file has the function to fetch token from .env file.
  To use this function one should import the library and
  call the function.
"""
import os
import warnings
from dotenv import load_dotenv


def setup(path: str = None,
          env_var: str = 'lichess_token'):
    """Function to fetch token from .env file.

    Parameters
    ----------
    path : str
        path of the .env file with the token.
    env_var : str
        variable name of the token inside the .env file.
    Returns
    -------
    str
        Token from lichess account to connect to API.
    """

    if path is not None:
        path = os.path.join(path, '.env')
    os.environ.clear()
    load_dotenv(dotenv_path=path, verbose=True)
    token = os.getenv(env_var)
    if token is None:
        warnings.warn("No token loaded.", Warning)
    return token
