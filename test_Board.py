import unittest
import numpy as np
import random
from Board import Board


class TestBoard(unittest.TestCase):

    def testConstructor(self):
        # pre Condition
        board = Board()

        # test
        self.assertEqual(board.board.all(), np.zeros((6, 7)).all())

    def testEnterPiece(self):
        # pre Condition
        board = Board()
        player1 = 1
        col = random.randint(0, 6)

        # test
        board.enterPiece(player1, col)

        # post Condition
        self.assertEqual(player1, board.board[5][col])

    def testSelectableColumns(self):
        # pre Condition
        board = Board()
        player1 = 1
        col = 1
        self.assertEquals(len(board.selectableColumns()), 7)

        # test
        for i in range(6):
            board.enterPiece(player1, col)

        # post Condition
        self.assertEquals(len(board.selectableColumns()), 6)
