from dotenv import load_dotenv
import os
import warnings
from pathlib import Path


def setup(path=None):
    # TODO: what if there isn't any key? It returns None
    if path is not None:
        path = os.path.join(path, '.env')
    load_dotenv(dotenv_path=path, verbose=True)
    token = os.getenv("lichess_token")
    if token is None:
        warnings.warn("No token loaded.", ResourceWarning)
    return token
