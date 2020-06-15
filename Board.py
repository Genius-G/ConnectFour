#!/usr/bin/python3

import numpy as np

class Board:
    """ Repräsentiert ein klassisches Vier Gewinnt Spielbrett """

    # Konstruktor
    def __init__(self):
        self.board = np.zeros((6, 7))
        self.players = [-1, 1]

    def enterPiece(self, player, col):
        """ fügt einen Spielstein in das Spielbrett in die Spalte "col" ein.
            Und simuliert dabei den Fall eines Spielsteines 
            Args:
                player[int] : liegt in {-1, 1}
                col[int] : liegt in {0, ..., 6}
            Returns:
                None
        """
        # überprüfe, ob eingegebene Spalte schon voll ist
        if col in self.selectableColumns():
            for row in range(5, -1, -1):
                # check from bottom to top where the entered piece stops
                if self.board[row][col] == 0:
                    self.board[row][col] = player
                    break
        
        # sage, wenn eine Spalte schon voll ist
        elif col in range(7):
            print("Spalte {} ist schon voll.".format(col))

        # sage, wenn col außerhalb liegt
        else:
            print("Spalte {} muss in {0, ..., 6} liegen.".format(col))
            
 
    def selectableColumns(self):
        """ gibt eine Teiliste der auswählbaren Spalten """

        selectableColumns = []
        for col in range(7):
            if self.board[0][col] == 0:
                selectableColumns.append(col)
        return selectableColumns

    def checkForStreak(self, player, streak):
        """ Überprüft auf Reihen der Länge "Streak" und gibt 
            dessen Vorkommen zurück.
            Args:
                player[int] : liegt in {-1, 1}
                streak[int] : liegt in {2, 3, 4}
            Returns:
                None
        """
        count = 0
        # für jeden Spielstein im Spielbrett ...
        for i in range(6):
            for j in range(7):

                # ... welches zum "player" gehört
                if self.board[i][j] == player:

                    # überprüfe auf vertikale Reihe bei (i, j)
                    count += self.verticalStreak(i, j, streak)
                    
                    # überprüfe auf horizontale Reihe bei (i, j)
                    count += self.horizontalStreak(i, j, streak)
                    
                    # überprüfe auf diagonale Reihe bei (i, j)
                    count += self.diagonalCheck(i, j, streak)

        # gebe die Summe der Reihen der Länge "streak" zurück
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
        # überprüfe für Diagonal mit positiver Steigung
        consecutiveCount = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break
            # erhöhe Spalte, wenn Reihe erhöht wird
            j += 1 
            
        if consecutiveCount >= streak:
            total += 1

        # überprüfe für Diagonal mit negativer Steigung
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j] == self.board[row][col]:
                consecutiveCount += 1
            else:
                break
            # erhöhe Spalte, wenn Reihe erhöht wird
            j += 1

        if consecutiveCount >= streak:
            total += 1

        return total

    def checkForWinner(self):
        """ überprüft auf Gewinner und gibt dann Wahr zurück """
        if self.checkForStreak(self.players[0], 4) > 0 or self.checkForStreak(self.players[1], 4) > 0:
            return True
        else:
            return False

    def checkForDraw(self):
        """ überprüft auf ein Unentschieden und gibt dann Wahr zurück """
        if len(self.selectableColumns()) == 0:
            return True
        else: 
            return False