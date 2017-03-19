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


if __name__ == '__main__':
    unittest.main()
