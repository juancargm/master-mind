""" Base application's controller for games interaction """
from flask import request
from app.controllers import endpoint_bp
from app.services import GameService


@endpoint_bp.before_app_first_request
def initialize_games():
    """ When the App starts, gets the games info from DB """
    GameService.initialize_games()

@endpoint_bp.route('/game/items/all', methods=['GET'])
def get_all_games():
    """Gets all the available games.

    Returns:
        Response: A Flask response object with all the available games.
    """
    return GameService.get_all()

@endpoint_bp.route('/game/guess', methods=['POST'])
def guess_code():
    """Does the guess for an user's game.

    Returns:
        Response: A Flask response object with the guess feedback.
    """
    content = request.json

    if content.get("user") and content.get("guess"):
        return GameService.guess_code(content.get("user"), content.get('guess'))
    else:
        return "Bad request: missing user or guess.", 400

@endpoint_bp.route('/game/reset/<string:user>', methods=['DELETE'])
def reset_game(user):
    """Resets an user's game if exists.

    Returns:
        Response: {}, 200.
    """
    GameService.reset_game(user)
    return {}, 200
