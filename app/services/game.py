""" Game Service """
from app.models import GameModel

class GameService(object):
    """ Service for the Game entity """
    @staticmethod
    def get_all():
        """Gets all the users games that have been played

        Returns:
            dict: {user: GameInfo} a dictionary with all the information
        """
        return GameModel.getAll()
    
    @staticmethod
    def add_game(user):
        """Adds a new game for a given user

        Args:
            user (str): username
        """
        GameModel.addGame(user, 'TEST')
