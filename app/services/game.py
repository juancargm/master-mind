""" Game Service """
import random

from collections import namedtuple
from flask import current_app as app
from app.models.game import GameInfo
from app.models import GameModel


class GameService(object):
    """ Service for the Game entity """
    games = {}
    colors = {}

    # Named tuple for readability
    Feedback = namedtuple('Feedback', ['black_pegs', 'white_pegs'])

    def __generate_game_solution():
        """Generates a new solution composed of 4 colors from those available in the App.

        Returns:
            str: the computed solution.
        """
        colors = app.config["AVAILABLE_COLORS"]
        random.shuffle(colors)

        if not app.config["ALLOW_DUPLICATES"]:
            solution = random.sample(colors, k=4)
        else:
            solution = random.choices(colors, k=4)

        return "".join(solution)
    
    def __is_valid_guess(guess):
        """Determines if an user guess is valid in length and colors

        Args:
            guess (str): the user's guess

        Returns:
            boolean: True if the guess is valid, false in any case.
        """
        if not guess or (guess and len(guess) != 4):
            return False
        else:
            for color in guess:
                if color not in GameService.colors:
                    return False
            
            return True
    
    def __get_solution_feedback(solution, guess):
        """Compares the user's prediction and generates corresponding feedback
        in black and white pegs.

        Args:
            solution (str): the user solution.
            guess (str): the user guess.

        Returns:
            Feedback: a tuple with the feedback based in the user guess.
        """
        r_sol = []
        r_guess = []

        black = 0
        white = 0

        if guess != solution:
            color = 0

            while color < 4:
                if guess[color] != solution[color]:
                    r_sol.append(solution[color])
                    r_guess.append(guess[color])
                else:
                    black += 1
                
                color += 1
            
            for item in r_guess:
                if item in r_sol:
                    white += 1
                    r_sol.remove(item)
      
        else:
            black = 4
        
        return GameService.Feedback(black, white)

    @staticmethod
    def reset_game(user):
        """Resets the game for an user

        Args:
            user (str): the user name
        """
        if user in GameService.games:
            GameModel.delete_game(user)
            GameService.games.pop(user)
            GameService.add_game(user)

    @staticmethod
    def initialize_games():
        """ Initializes the object in memory with the DB information,
        to gets persistance in case of shut down. """
        GameService.games = GameModel.get_all()
        # Build a set to do the guess check
        GameService.colors = {color for color in app.config["AVAILABLE_COLORS"]}

    @staticmethod
    def get_all():
        """Gets all the users games that have been played.

        Returns:
            dict: {user: GameInfo} a dictionary with all the information.
        """
        return GameService.games
 
    @staticmethod
    def add_game(user):
        """Adds a new game for a given user.

        Args:
            user (str): the username.
        """
        solution = GameService.__generate_game_solution()
        GameModel.add_game(user, solution)
        GameService.games[user] = GameInfo(solution, 0)

    @staticmethod
    def guess_code(user, guess):
        """Determines if an user guesses his code and generate the feedback

        Args:
            user (str): the user name
            guess (str): the guess

        Returns:
            Response: Flask response (body and status code)
        """
        if GameService.__is_valid_guess(guess):
            if user not in GameService.games:
                # Start new game for that user and persist the game in DB
                GameService.add_game(user)
            elif GameService.games[user].attempts == app.config["ATTEMPTS"]:
                # The user losses in his last move, so the game resets
                GameService.reset_game(user)
            
            feedback = GameService.__get_solution_feedback(GameService.games[user].solution, guess)

            # Register the attempt
            GameService.games[user] = GameInfo(GameService.games[user].solution, GameService.games[user].attempts + 1)

            # Persist the game status in DB
            GameModel.update_game_attemps(user, GameService.games[user].attempts)

            # Determine if the user wins
            user_wins = feedback.black_pegs == 4

            # Determine if the maximum attempts reached, the user losses
            user_has_lost = GameService.games[user].attempts == app.config["ATTEMPTS"] and not user_wins

            # Generate the response
            response = {
                "black_pegs": feedback.black_pegs,
                "white_pegs": feedback.white_pegs,
                "remaining_attempts": app.config["ATTEMPTS"] - GameService.games[user].attempts,
                "user_wins": user_wins,
                "user_has_lost": user_has_lost
            }

            if user_wins:
                GameService.reset_game(user)

            return response, 200
        else:
            # Report the error to the user
            return "The guess has an invalid format.", 500

