import os
import warnings
from dotenv import load_dotenv


def setup(path=None):
    env_var = 'lichess_token'
    DB_dir = 'resources/PGN_database'
    if not os.path.isdir(DB_dir):
        os.makedirs(DB_dir)
    if path is not None:
        path = os.path.join(path, '.env')
    os.environ.clear()
    load_dotenv(dotenv_path=path, verbose=True)
    token = os.getenv(env_var)
    if token is None:
        warnings.warn("No token loaded.", ResourceWarning)
    return token
