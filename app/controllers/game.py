""" Base application's controller for games interaction """
from app.controllers import endpoint_bp
from app.services import GameService


@endpoint_bp.route('/game/items/all', methods=['GET'])
def get_all_games():
    """Gets all the available games.

    Returns:
        Response: A Flask response object with all the available games
    """
    return GameService.get_all()
