""" Application config variables. """
import os


# Ensure the app.db file will be in the App directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """ Class for link the config variables to Flask. """
    ATTEMPTS = 10
    AVAILABLE_COLORS = {'R', 'B', 'Y', 'G', 'W', 'O'}
    ALLOW_DUPLICATES = True

    # SQL Alchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'app.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
