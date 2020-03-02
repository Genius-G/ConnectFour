"""
This class represents a board used in a typical 'ConnectFour' Game
"""
import numpy as np


class Board:

    # Constructor
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = np.zeros((height, width))

    # Enter a piece to the board
    def enterPiece(self, player, col):
        # check if desired col is full
        if col in self.selectableColumns():
            for row in range(self.height):
                # check from bottom to top where entered piece stops
                if self.board[row][col] == 0:
                    self.board[row][col] = player
        else:
            # give back some kind of error
            print('%d is already full', col)

    # Check For a Winner
    def checkForWinner(self):
        return self.checkVertically() + self.checkHorizontally() + \
               self.checkDiagonallyFalling() + self.checkDiagonallyRising()

    # Check rows for winner
    def checkHorizontally(self):
        for row in range(self.height):
            for col in range(self.width - 3):
                if (self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] ==
                        self.board[row][col + 3]) and (self.board[row][col] != " "):
                    return self.board[row][col]

    # Check columns for winner
    def checkVertically(self):
        for col in range(self.height):
            for row in range(self.width - 3):
                if (self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] ==
                        self.board[row + 3][col]) and (self.board[row][col] != " "):
                    return self.board[row][col]

    # Check diagonal (top-left to bottom-right) for winner
    def checkDiagonallyFalling(self):
        for row in range(self.height - 3):
            for col in range(self.width -3):
                if (self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] ==
                        self.board[row + 3][col + 3]) and (self.board[row][col] != " "):
                    return self.board[row][col]

    # Check diagonal (bottom-left to top-right) for winner
    def checkDiagonallyRising(self):
        for row in range(self.height - 1, 2, -1):
            for col in range(3):
                if (self.board[row][col] == self.board[row - 1][col + 1] == self.board[row - 2][col + 2] ==
                        self.board[row - 3][col + 3]) and (self.board[row][col] != " "):
                    return self.board[row][col]

    # ToDo create method
    def selectableColumns(self):
        pass