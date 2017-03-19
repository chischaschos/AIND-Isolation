"""
This file contains all the scoring strategies.

- The best position a player can have has 8 legal movements.

    |   | x |   | x |   |
    | x |   |   |   | x |
    |   |   | P |   |   |
    | x |   |   |   | x |
    |   | x |   | x |   |

- A wall our board boundary decreases the amount of available movements starting with
  2, 3, 4, 4 and 6.

    | P |   |   |   |   |
    |   |   | x |   |   |
    |   | x |   |   |   |
    |   |   |   |   |   |
    |   |   |   |   |   |

    |   |   | x |   |   |
    | P |   |   |   |   |
    |   |   | x |   |   |
    |   | x |   |   |   |
    |   |   |   |   |   |

    |   | x |   |   |   |
    |   |   | x |   |   |
    | P |   |   |   |   |
    |   |   | x |   |   |
    |   | x |   |   |   |

    |   |   |   |   |   |
    | x |   | x |   |   |
    |   |   |   | x |   |
    |   | P |   |   |   |
    |   |   |   | x |   |

    | x |   | x |   |   |
    |   |   |   | x |   |
    |   | P |   |   |   |
    |   |   |   | x |   |
    | x |   | x |   |   |
"""

import pdb
# import sample_players

def toe_stepper_score(game, player):
    opponent = game.get_opponent(player)
    opponent_location = game.get_player_location(opponent)
    player_location = game.get_player_location(player)

    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]

    score = 0
    for direction in directions:
        position = (player_location[0] + direction[0],
                    player_location[1] + direction[1])

        if position == opponent_location:
            score += __move_value() * 2
            break

    return score


def toe_stepper(game, player):
    """
    open_move_score plus:
    - Figures out the opponent's position.
    - See if the player is on a opponent's location.
    - If it is we score the game higher because the movement that lead to this
      game reduced the opponent's movements.

    - Pros:
      - Gives a higher score to movements that would reduce the other player's
        number of moves.
    - Cons:
      - Could end up in disadvantage if after the movement the other
        user has same or more movements that him.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    open_move_score = float(len(game.get_legal_moves(player))) * 10

    return open_move_score + toe_stepper_score(game, player)


def improved_toe_stepper(game, player):
    """
    improved_score + toe_stepper idea

    The idea is that games where the player has more movements are better.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    improved_score = float(own_moves - opp_moves)

    return improved_score + toe_stepper_score(game, player)


def common_sense(game, player):
    """
    The idea is:
    - Give weights to different  factors of the game
    - Builds on toe_stepper and improved_score plus
    - There are movements that can block an opponent's next move such as:
      |   |   |   |   |   |   |   |
      |   |   |   |   | o |   |   |
      |   |   | O |   |   |   |   |
      |   |   |   | P |   |   |   |
      |   | o |   |   |   |   |   |
      |   |   |   |   |   |   |   |
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    improved_score = float(own_moves - opp_moves) * 10

    opponent = game.get_opponent(player)
    opponent_location = game.get_player_location(opponent)
    player_location = game.get_player_location(player)

    diagonal_directions = [(-1, -1), (1, -1), (1, -1), (1, 1)]

    diagonal_score = 0

    for d_direction in diagonal_directions:
        position = (player_location[0] + d_direction[0],
                    player_location[1] + d_direction[1])

        if position == opponent_location:
            diagonal_score += __move_value() * 2

    return improved_score + diagonal_score + toe_stepper_score(game, player)


def __move_value():
    return round(1 / 8 * 100)


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
    return common_sense(game, player)
