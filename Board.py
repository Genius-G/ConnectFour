#!/usr/bin/python3

import numpy as np

class Board:
    """ This class represents a board used in a standart ConnectFour Game """

    # Constructor
    def __init__(self):
        self.board = np.zeros((6, 7))
        self.colors = [-1, 1]

    # Enter a piece to the board
    def enterPiece(self, player, col):
        """ enter a piece the board """
        # check if desired col is full
        if col in self.selectableColumns():
            for row in range(5, -1, -1):
                # check from bottom to top where entered piece stops
                if self.board[row][col] == 0:
                    self.board[row][col] = player
                    break
        else:
            print("%d ist schon voll.", col)

    def selectableColumns(self):
        """ give a list of all selectable columns """
        selectableColumns = list(range(7))
        for col in range(7):
            if self.board[0][col] != 0 and col in selectableColumns:
                selectableColumns.remove(col)
        return selectableColumns

    # check for number of streaks of length streak: (int)
    def checkForStreak(self, color, streak):
        count = 0
        # for each piece in the board...
        for i in range(6):
            for j in range(7):
                # ...that is of the color we're looking for...
                if self.board[i][j] == color:
                    # check if a vertical streak starts at (i, j)
                    count += self.verticalStreak(i, j, streak)
                    
                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += self.horizontalStreak(i, j, streak)
                    
                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += self.diagonalCheck(i, j, streak)
        # return the sum of streaks of length 'streak'
        return count
            
    def verticalStreak(self, row, col, streak):
        consecutiveCount = 0
        for i in range(row, 6):
            if self.board[i][col] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break
    
        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    
    def horizontalStreak(self, row, col, streak):
        consecutiveCount = 0
        for j in range(col, 7):
            if self.board[row][j] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0
    
    def diagonalCheck(self, row, col, streak):

        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented
            
        if consecutiveCount >= streak:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break
            j += 1 # increment column when row is incremented

        if consecutiveCount >= streak:
            total += 1

        return total

    # Check For a Winner
    def checkForWinner(self):       
        if self.checkForStreak(self.colors[0], 4) > 0 or self.checkForStreak(self.colors[1], 4) > 0:
            return True
        else:
            return False

    # Check For a Draw
    def checkForDraw(self):
        if len(self.selectableColumns()) == 0:
            return True
        else: 
            return False