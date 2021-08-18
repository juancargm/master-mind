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
    def get_all():
        """Gets all the users games that have been played

        Returns:
            dict: {user: GameInfo} a dictionary with all the information
        """
        return {game.user: GameInfo(game.solution, game.attempts) for game in Game.query.all()}

    @staticmethod
    def add_game(user, solution):
        """Adds a new game for a given user

        Args:
            user (str): username
            solution (str): the game solution
        """
        new_game = Game(user=user, solution=solution, attempts=0)
        db.session.add(new_game)
        db.session.commit()

    @staticmethod
    def delete_game(user):
        """Remove an user's game

        Args:
            user (str): the user name.
        """
        db.session.query(Game).filter_by(user=user).delete()
        db.session.commit()

    @staticmethod
    def update_game_attemps(user, attemps):
        """Update the number of attemps made in a Game

        Args:
            user (str): the user.
            attemps (int): the new number of attempts.
        """
        db.session.query(Game).filter_by(user=user).update({"attempts": attemps})
        db.session.commit()
