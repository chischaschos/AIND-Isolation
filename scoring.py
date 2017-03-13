"""
This file contains all the scoring strategies
"""

import pdb

def toe_stepper(game, player):
    """
    - Based on number_of_moves.
    - PRO: Gives a higher score to movements that would reduce the other player's
    number of moves.
    - CONS: could end up in disadvantage if after the movement the other
    user has same or more movements that him
    - how to score it?, twice moves?, plus X extra score?
      - if doubling score it could prefer games where:
        - it would prefer taking a movement away from the user to
        move to a posistion of more movements such as

    - Let's try giving two points if there is a position that would reduce
    the opponents movement
    - Then ensure that we do not end up in disadvantage
    """
    score = number_of_moves(game, player)
    opponent = game.get_opponent(player)
    opponent_location = game.get_player_location(opponent)
    player_location = game.get_player_location(player)

    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2),  (1, 2), (2, -1),  (2, 1)]

    for l in directions:
        nm = (player_location[0] + l[0], player_location[1] + l[1])

        # pdb.set_trace()
        # see player available moves, see if I'm in one of the moves that he could
        if nm == opponent_location:
            # we stepped on an opponents position
            score += 2
            break

    return score

def greedy_toe_stepper(game, player):
    legal_moves = game.get_legal_moves(player)
    if not legal_moves:
        return 0

    score = max([toe_stepper(game.forecast_move(m), player) for m in legal_moves])
    score += toe_stepper(game, player)

    return score


def number_of_moves(game, player):
    """
    Calculates a score based on the number of available moves for the current
    player
    """
    return float(len(game.get_legal_moves()))


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    return greedy_toe_stepper(game, player)
