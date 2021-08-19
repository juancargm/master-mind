# Mastermind game API implementation

Lightweight Python Flask API for implementing the mastermind game.


# Getting Started


## Enviroment variables

The App needs to set the following variables:

* FLASK_APP: **(required)** run.py.
* ATTEMPTS: number of attempts for a game, default is 10.
* AVAILABLE_COLORS: list with the colors to be used. The format should be a string list with a letter in each position representing the color, default is ['R', 'B', 'Y', 'G', 'W', 'O'].
* ALLOW_DUPLICATES: allows the solution to have duplicate or non-duplicate colors, default is True.
* SQLALCHEMY_DATABASE_URI: database URL, if not specified a local sql-lite database will be used to avoid losing items due to an unexpected server shutdown.

## Intallation

This APP requires Python 3.X. In the App directory:

1. `$ git clone https://github.com/juancargm/master-mind.git`.
2. `cd master-mind`.
3. `$ pip install virtualenv` (if not installed).
4. `$ virtualenv venv`.
5. `$ .\venv\Scripts\activate.bat` | `source venv/bin/activate`.
6. `$ pip install -r requirements.txt`.
7. `$ set FLASK_APP=run.py` | `$ export FLASK_APP=run.py`.
8. `$ flask run`.
