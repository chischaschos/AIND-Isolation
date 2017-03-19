"""
Simple tests for scoring functions
"""

import unittest

import isolation
import game_agent

import scoring


class ScoringTest(unittest.TestCase):
    """
    Simple tests for scoring functions
    """

    def test_toe_stepper(self):
        """
        | 2 |   |   |   | x |   |   |
        |   |   | 1 |   |   |   |   |
        | x |   |   |   | x |   |   |
        |   | x |   | x |   |   |   |
        |   |   |   |   |   |   |   |
        |   |   |   |   |   |   |   |
        """
        agent_ut = game_agent.CustomPlayer()
        board = isolation.Board(agent_ut, 'null_agent')

        starting_location = (1, 2)
        adversary_location = (0, 0)
        board.apply_move(starting_location)
        board.apply_move(adversary_location)

        score = scoring.toe_stepper(board, board.active_player)

        self.assertEqual(score, 74)

    def test_common_sense_1(self):
        """
        - Player 1 has 5 movements,  Player 2 has 1 movement:
          - 5 - 1 = 4 * maximizer = 40
        - Player 1's movement stepped on an Player 2's move:
          - score += 1 * mov_value * maximizer ~ 24

        | 2 |   |   |   | x |   |   |
        |   |   | 1 |   |   |   |   |
        | x |   |   |   | x |   |   |
        |   | x |   | x |   |   |   |
        |   |   |   |   |   |   |   |
        |   |   |   |   |   |   |   |
        """
        agent_ut = game_agent.CustomPlayer()
        board = isolation.Board(agent_ut, 'null_agent')

        starting_location = (1, 2)
        adversary_location = (0, 0)
        board.apply_move(starting_location)
        board.apply_move(adversary_location)

        score = scoring.common_sense(board, board.active_player)

        self.assertEqual(score, 64)


    def test_common_sense_2(self):
        """
        - Player O has 8 movements,  Player P has 8 movement:
          - 8 - 8 = 0
        - Player P's may block an opponents next move
          - score += __mov_value * 2 = 24

        |   |   | o | p | o | p |   |
        |   | o |   |   |   | o |   |
        |   |   | p | O |   |   | p |
        |   | o |   |   | P | o |   |
        |   |   | x |   | o |   | p |
        |   |   |   | p |   | p |   |
        """
        agent_ut = game_agent.CustomPlayer()
        board = isolation.Board(agent_ut, 'null_agent')

        starting_location = (3, 4)
        adversary_location = (2, 3)
        board.apply_move(starting_location)
        board.apply_move(adversary_location)

        score = scoring.common_sense(board, board.active_player)

        self.assertEqual(score, 24)

    def test_common_sense_3(self):
        """
        - Player O has 2 movements,  Player P has 4 movement:
          - 4 - 2 = 2 * 10 = 20

        |   |   |   |   |   |   |   |
        |   |   |   |   |   |   |   |
        |   |   |   |   | p |   | p |
        |   |   |   | p |   | o |   |
        |   |   |   |   | o | P |   |
        |   |   |   | p |   |   | O |
        """
        agent_ut = game_agent.CustomPlayer()
        board = isolation.Board(agent_ut, 'null_agent')

        starting_location = (5, 5)
        adversary_location = (6, 6)
        board.apply_move(starting_location)
        board.apply_move(adversary_location)

        score = scoring.common_sense(board, board.active_player)

        self.assertEqual(score, 20)

    def test_common_sense_4(self):
        """
        - Player O has 2 movements,  Player P has 6 movement:
          - 6 - 4 = 2 * 10 = 20
        - Player P's may block an opponents next move
          - score += __mov_value * 2 = 24

        |   |   |   |   |   |   |   |
        |   |   |   |   | p |   | p |
        |   |   |   | p |   | o |   |
        |   |   |   |   | o | P |   |
        |   |   |   | p |   |   | O |
        |   |   |   |   | x |   | p |
        |   |   |   |   |   | o |   |
        """
        agent_ut = game_agent.CustomPlayer()
        board = isolation.Board(agent_ut, 'null_agent')

        starting_location = (3, 5)
        adversary_location = (4, 6)
        board.apply_move(starting_location)
        board.apply_move(adversary_location)

        score = scoring.common_sense(board, board.active_player)

        self.assertEqual(score, 44)


    def test_common_sense_5(self):
        """
        - Player O has 3 movements,  Player P has 6 movement:
          - 6 - 3 = 3 * 10 = 30
        - Player P's may block an opponents next move
          - score += __mov_value * 2 = 24

        |   |   |   |   | x |   | p |
        |   |   |   | p |   |   | O |
        |   |   |   |   | o | P |   |
        |   |   |   | p |   | o |   |
        |   |   |   |   | p |   | p |
        |   |   |   |   |   |   |   |
        |   |   |   |   |   |   |   |
        """
        agent_ut = game_agent.CustomPlayer()
        board = isolation.Board(agent_ut, 'null_agent')

        starting_location = (2, 5)
        adversary_location = (1, 6)
        board.apply_move(starting_location)
        board.apply_move(adversary_location)

        score = scoring.common_sense(board, board.active_player)

        self.assertEqual(score, 54)


if __name__ == '__main__':
    unittest.main()
