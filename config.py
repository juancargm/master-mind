""" Application config variables. """
import os
from ast import literal_eval


# Ensure the app.db file will be in the App directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ Class for linking the config variables to Flask. """
    ATTEMPTS = int(os.environ.get('ATTEMPTS', 10))
    AVAILABLE_COLORS = literal_eval(os.environ.get('AVAILABLE_COLORS', "['R', 'B', 'Y', 'G', 'W', 'O']"))
    ALLOW_DUPLICATES = literal_eval(os.environ.get('ALLOW_DUPLICATES', "True"))
    TESTING = False

    # SQL Alchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'app.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
