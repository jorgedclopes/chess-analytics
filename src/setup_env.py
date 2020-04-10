from dotenv import load_dotenv
import os
import warnings


def setup(path=None):
    env_var = 'lichess_token'
    if path is not None:
        path = os.path.join(path, '.env')
    os.environ.clear()
    load_dotenv(dotenv_path=path, verbose=True)
    token = os.getenv(env_var)
    if token is None:
        warnings.warn("No token loaded.", ResourceWarning)
    return token
