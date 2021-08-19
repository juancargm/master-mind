""" Tests for the app. """
import os
import tempfile

import pytest

from app import init_app
from app.services import GameService


@pytest.fixture
def client():
    """ Prepare the App for testing. """
    db_fd, db_path = tempfile.mkstemp()
    app = init_app({'TESTING': True,
                    'SQLALCHEMY_DATABASE_URI': f"sqlite:///{db_path}",
                    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
                    'ATTEMPTS': 10,
                    'AVAILABLE_COLORS': ['R', 'B', 'Y', 'G', 'W', 'O'],
                    'ALLOW_DUPLICATES': True,
                    })

    with app.test_client() as client:
        with app.app_context():
            init_app()
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_empty_db(client):
    """ Start with an empty database. """

    rv = client.get('/game/items/all')
    assert not rv.json, "DB should be empty."

def test_reset(client):
    """ Check if the reset works properly. """
    rv = client.delete(f'/game/reset/@test_user@')

    # Checks if the game is properly reset
    rv = client.post(f'/game/guess', json={"user": "@test_user@", "guess": "BBBB"})
    assert rv.json.get("remaining_attempts") == 9, "Remaining attempts should be 9."

def test_valid_guess_lenght(client):
    """ Check if the guess length is validated properly. """
    rv = client.post(f'/game/guess', json={"user": "@test_user@", "guess": "BBBBBBB"})
    assert b'The guess has an invalid format.' in rv.data

def test_valid_guess_format(client):
    """ Check if the guess format is validated properly. """
    rv = client.post(f'/game/guess', json={"user": "@test_user@", "guess": "_@#$"})
    assert b'The guess has an invalid format.' in rv.data

def test_is_valid_guess(client):
    """ Check if a good guess is accepted. """
    rv = client.post(f'/game/guess', json={"user": "@test_user@", "guess": "RBRB"})
    assert rv.json, "A JSON with the feedback should be returned."

def test_solution_generator(client):
    """ Check if the solution is generated properly. """
    # Do a request for initialize de App propperly.
    client.delete(f'/game/reset/@test_user@')

    solution = GameService.generate_game_solution()

    assert GameService.is_valid_guess(solution), "The solution should have a correct lenght and colors."

def test_feedback(client):
    # Do a request for initialize de App propperly.
    client.delete(f'/game/reset/@test_user@')

    feedback_is_good = True
    fail_idx = -1
    idx = 0

    solutions = ['RGGB', 'RRRR', 'GBBR', 'BBBR', 'RBGG', 'RBGW']
    guesses = ['RGGB', 'BYOB', 'GBRB', 'RBGG', 'BBBR', 'BBBB']
    perfect_feedback = [GameService.Feedback(4, 0),
                        GameService.Feedback(0, 0),
                        GameService.Feedback(2, 2),
                        GameService.Feedback(1, 1),
                        GameService.Feedback(1, 1),
                        GameService.Feedback(1, 0)]

    while idx < 6 and feedback_is_good:
        feedback = GameService.get_solution_feedback(solutions[idx], guess=guesses[idx])

        if (feedback.black_pegs != perfect_feedback[idx].black_pegs or
                feedback.white_pegs != perfect_feedback[idx].white_pegs):
            feedback_is_good = False
            fail_idx = idx

        idx += 1

    assert feedback_is_good, f"The feedback with index {fail_idx} is not correct."
