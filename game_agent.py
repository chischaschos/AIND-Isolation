"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import pdb
from collections import deque
from scoring import custom_score


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: create opening book based on the legal_moves param?
        # TODO: return immediately if there are no legal moves?
        next_move = None
        depth = 1
        search_method = self.minimax if self.method is 'minimax' else self.alphabeta

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.iterative:

                # TODO: I suppose that at some point I need to make sure that
                # given X remaining time I can estimate that the next loop
                # iteration will end.
                # I may be wrong because the Timeout is raised when the timer
                # is closed to expiring
                while True:
                    if self.time_left() < self.TIMER_THRESHOLD:
                        return next_move
                    _, next_move = search_method(game, depth)
                    depth += 1
            else:
                _, next_move = search_method(game, depth)
                return next_move

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return next_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        nm = [(float("-inf"), (-1, -1))]

        for move in game.get_legal_moves():
            game_child = game.forecast_move(move)
            nm.append((self.__mm_min_value(game_child, depth - 1), move))

        return max(nm)


    def __mm_min_value(self, game, depth):
        if self.__cutoff_test(game, depth):
            return self.score(game, game.__player_1__)

        value = float("+inf")
        for move in game.get_legal_moves():
            game_child = game.forecast_move(move)
            value = min(value, self.__mm_max_value(game_child, depth - 1))

        return value

    def __mm_max_value(self, game, depth):
        if self.__cutoff_test(game, depth):
            return self.score(game, game.__player_1__)

        value = float("-inf")
        for move in game.get_legal_moves():
            game_child = game.forecast_move(move)
            value = max(value, self.__mm_min_value(game_child, depth - 1))

        return value


    def __cutoff_test(self, game, depth):
        """
        Assumming that get_legal_moves returns the available legal move for the current min or max player
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        return not game.get_legal_moves() or depth == 0



    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        best_move = (-1, -1)

        for move in game.get_legal_moves():
            game_child = game.forecast_move(move)
            value = self.__ab_min_value(game_child, depth - 1, alpha, beta)

            if value >= alpha:
                alpha, best_move = value, move

        return alpha, best_move


    def __ab_min_value(self, game, depth, alpha, beta):
        if self.__cutoff_test(game, depth):
            return self.score(game, game.__player_1__)

        value = float("+inf")
        for move in game.get_legal_moves():
            value = min(value, self.__ab_max_value(game.forecast_move(move), depth - 1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    def __ab_max_value(self, game, depth, alpha, beta):
        if self.__cutoff_test(game, depth):
            return self.score(game, game.__player_1__)

        value = float("-inf")
        for move in game.get_legal_moves():
            value = max(value, self.__ab_min_value(game.forecast_move(move), depth - 1, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)

        return value
