""" Game entity """
from collections import namedtuple
from app import db

# Named tuple for readability
GameInfo = namedtuple('GameInfo', ['solution', 'attempts'])

class Game(db.Model):
    """ Entity for saving the users games """
    __tablename__ = 'game'
    __table_args__ = {"extend_existing": True}

    user = db.Column(db.String(32), primary_key=True)
    # The solution will be composed of 4 values,
    # and the number of possible values can be configured in the application.
    solution = db.Column(db.String(4))
    attempts = db.Column(db.Integer)

class GameModel(object):
    """ Model for performing operations on the entity Game """
    @staticmethod
    def getAll():
        """Gets all the users games that have been played

        Returns:
            dict: {user: GameInfo} a dictionary with all the information
        """
        return {game.user: GameInfo(game.solution, game.attempts) for game in Game.query.all()}

    @staticmethod
    def addGame(user, solution):
        """Adds a new game for a given user

        Args:
            user (str): username
            solution (str): the game solution
        """
        new_game = Game(user=user, solution=solution, attempts=0)
        db.session.add(new_game)
        db.session.commit()
