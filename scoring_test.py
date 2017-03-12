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

    def test_number_of_moves(self):
        """
        Test that player 1 has 8 available moves from a position with this
        characteristics:
          - Far from a wall
          - Not colliding with a player or used space
        | 2 |   |   |   | x |   |   |
        |   |   | 1 |   |   |   |   |
        | x |   |   |   | x |   |   |
        |   | x |   | x |   |   |   |
        |   |   |   |   |   |   |   |
        |   |   |   |   |   |   |   |
        |   |   |   |   |   |   |   |
        """
        agent_ut = game_agent.CustomPlayer()
        board = isolation.Board(agent_ut, 'null_agent')

        starting_location = (1, 2)
        adversary_location = (0, 0)
        board.apply_move(starting_location)
        board.apply_move(adversary_location)
        print(board.to_string())

        score = scoring.number_of_moves(board, board.active_player)

        self.assertEqual(score, 5)

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

        self.assertEqual(score, 5 + 2)
if __name__ == '__main__':
    unittest.main()
