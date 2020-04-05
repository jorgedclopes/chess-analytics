from dotenv import load_dotenv
import os


def setup():
    # TODO: what if there isn't any key?
    load_dotenv()
    TOKEN = os.getenv("lichess_token")
    return TOKEN
