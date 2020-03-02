#!/usr/bin/python3

'''
version 0.1 - 10.Jan 2020

Der Code enthält bisher:
    Methoden für...
    ... eine Bildschirmausgabe
    ... das Platzieren eines Chips
    ... zufällige Züge
    ... das Überprüfen eines Zuges auf Win States   (effizient, limitiert)
    ... das Überprüfen eines Boardes auf Win States (ineffizient, universal)

Es fehlen:
    Methoden für...
    ... das Evaluieren potentieller Spielzüge
    ... die Auswahl eines Spielzuges anhand vorheriger Evaluationen
    ... die Interaktion mit dem Roboter (wartet auf finales Design)

Weiteres Vorgehen:
    Der Algorithmus soll anhand versteckter Spielbretter n Züge (n < 5) in
    die Zukunft sehen und entscheiden, welcher Weg durch die Spielzüge ihm
    die größte Chance auf einen Sieg verschafft. Dazu kann auch berücksich-
    tigt werden, dass in Connect 4 "Fallen" existieren, was theoretisch so-
    gar die Vorhersage eines Sieges in mehr als n Zügen erlaubt.
    Weiterhin sollen nach Fertigstellung eines funktionierenden Konzepts
    des Roboters die Methoden zur Steuerung der Motoren hier implementiert
    werden.
'''

import random
import numpy as np
from colorama import Fore, Back, Style


# Setup –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
board = np.zeros((7,6)) # erstellt Spielbrett (einfachkeitshalber transponiert)
columns = np.full(7,6)  # 6 statt 5 für Verständlichkeit ("n freie Felder")
#player = -1             # legt den aktuellen Spieler fest {-1, 1}
player = random.choice([-1,1])
counter = 0

#print(board.T)
#print(columns)


# Display functions –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
def showBoard(board):
    for j in range(6):
        printstring = ""
        for i in range(7):
            if board[i][j] == 0:
                printstring += " 0 "
            if board[i][j] == 1:
                printstring += "\u001b[41;1m\u001b[31m 1 \u001b[0m\u001b[0m"
            if board[i][j] == -1:
                printstring += "\u001b[43;1m\u001b[33m-1 \u001b[0m\u001b[0m"

        print(printstring)
    #print(board)            # nicht transponiert (technische Ansicht)

def showIndicators():
    print("_1__2__3__4__5__6__7_")

def showColumns(columns):
    printstring = ""
    for i in range(7):
        printstring += " " + str(columns[i]) + " "
    print(printstring)


# Board Interaction –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
def placeCoin(board, col, player):                  #Führt einen Zug aus
    if (col >= 0 and col <= 6):
        if columns[col] >= 1:
            board[col][columns[col]-1] = player
            columns[col] -= 1

            showIndicators()
            showBoard(board)
            #showColumns(columns)

            return player * -1

        else:
            print("Ungültige Eingabe! (Zeile voll)")
            return player

    else:
        print("Ungültige Eingabe! (out of range)")
        #break
        return player


# AI stuff ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
def randomMove(board, columns, player):
    while True:
        col = random.choice(range(7))
        if columns[col] > 0:
            print(col)
            return col + 1

def calculateResponses(board, columns, player):
    #_board = board
    #_columns = columns
    #_player = player

    for col in range(7):
        _board = board
        _columns = columns
        _player = player
        if _columns[col] > 0:
            _player = placeCoin(_board, col, _player)


# Check win cases by move –––––––––––––––––––––––––––––––––––––––––––––––––––––
def checkVertical(board, col):
    if columns[col] <= 2:
        value = board[col][columns[col]]
        if board[col][columns[col]+1] == value:
            if board[col][columns[col]+2] == value:
                if board[col][columns[col]+3] == value:
                    return True
    return False

def checkHorizontal(board, col):
    """row = columns[col]
    value = board[col][row]
    for i in range(4):
        if board[i][row] == value:
            if board[i+1][row] == value:
                if board[i+2][row] == value:
                    if board[i+3][row] == value:
                        return True
    return False"""

    row = columns[col]
    value = board[col][row]
    wincount = 0

    i = col + 1
    while i <= 6 and i <= col+3:
        if board[i][row] == value:
            wincount += 1
            #print(">",i)
            if wincount == 3:
                return True
        else:
            break
        i += 1

    i = col - 1
    while i >= 0 and i >= col-3:
        if board[i][row] == value:
            wincount += 1
            #print("<",i)
            if wincount == 3:
                return True
        else:
            break
        i -= 1
    return False

def checkRisingDiagonal(board, col):
    row = columns[col]
    value = board[col][row]
    wincount = 0

    i = col + 1
    j = row - 1
    while i <= 6 and j >= 0 and i <= col+3:
        if board[i][j] == value:
            wincount += 1
            #print("^",i,j, wincount)
            if wincount == 3:
                return True
        else:
            break
        i += 1
        j -= 1

    i = col - 1
    j = row + 1
    while i >= 0 and j <= 5 and i >= col-3:
        if board[i][j] == value:
            wincount += 1
            #print("v",i,j, wincount)
            if wincount == 3:
                return True
        else:
            break
        i -= 1
        j += 1

    return False

def checkFallingDiagonal(board, col):
    row = columns[col]
    value = board[col][row]
    wincount = 0

    i = col - 1
    j = row - 1
    while i >= 0 and j >= 0 and i >= col-3:
        if board[i][j] == value:
            wincount += 1
            #print("^",i,j, wincount)
            if wincount == 3:
                return True
        else:
            break
        i -= 1
        j -= 1

    i = col + 1
    j = row + 1
    while i <= 6 and j <= 5 and i <= col+3:
        if board[i][j] == value:
            wincount += 1
            #print("v",i,j, wincount)
            if wincount == 3:
                return True
        else:
            break
        i += 1
        j += 1

    return False

def checkDraw(columns):
    if sum(columns) == 0:
        return True

    return False


# Check win cases by board ––––––––––––––––––––––––––––––––––––––––––––––––––––
def checkBoardVertical(board):
    for col in range(7):
        wincount = 0
        value = 0
        for row in range(6):
            if value == board[col][row]:
                wincount += 1
            else:
                wincount = 0
                value = board[col][row]
                continue
            if wincount == 4:
                return True, col, row, value
    return False, 0, 0, 0

def checkBoardHorizontal(board):
    for row in range(6):
        wincount = 0
        value = 0
        for col in range(7):
            if value == board[col][row] and value != 0:
                wincount += 1
            else:
                wincount = 0
                value = board[col][row]
                continue
            if wincount == 4:
                return True, col, row, value
    return False, 0, 0, 0

def checkBoardRising(board):
#      * * * *       * * * *
#     * * * * *      * * * *
#    * * * * * *  →  * * * * *
#    * * * * * *     * * * * *
#     * * * * *      * * * * * *
#      * * * *       * * * * * *
#        ...         ...
    sze = len(board) -1
    for i in range(3, sze):
        print("/",i)
        col = 0
        row = i
        value = board[col][row]
        wincount = 0
        while row >= 0:
            print(" 1) check row", row)
            if board[col][row] != 0:
                if value == board[col][row]:
                    wincount += 1
                    if wincount == 4:
                        print(col, row, value)
                        return True, col, row, value
                elif row <= 2:
                    row = 0
            elif row <= 3:
                    row = 0
            else:
                wincount = 0
                value = board[col][row]
            col += 1
            row -= 1

        col = sze-i
        row = len(board[1])-1
        value = board[col][row]
        wincount = 0
        while col <= sze:
            print(" 2) check")
            if board[col][row] != 0:
                if value == board[col][row]:
                    wincount += 1
                    if wincount == 4:
                        print(col, row, value)
                        return True, col, row, value
                elif col >= sze - 2:
                    col = sze
            elif col >= sze - 3:
                col = sze
            else:
                wincount = 0
                value = board[col][row]
            col += 1
            row -= 1

    return False, 0, 0, 0

def checkBoardFalling(board):
    sze = len(board) -1
    for i in range(3, sze):
        print("\\",i)
        col = sze
        row = i
        value = board[col][row]
        wincount = 0
        while row >= 0:
            print(" 1) check row:",row)
            if board[col][row] != 0:
                if value == board[col][row]:
                    wincount += 1
                    if wincount == 4:
                        print(col, row, value)
                        return True, col, row, value
                elif row <= 2:
                    row = 0
                else:
                    wincount = 0
                    value = board[col][row]
            elif row <= 3:
                    row = 0
            else:
                wincount = 0
                value = board[col][row]
            col -= 1
            row -= 1

        col = sze-i
        row = len(board[1])-1
        value = board[col][row]
        wincount = 0
        while col >= 0:
            print(" 2) check")
            if board[col][row] != 0:
                if value == board[col][row]:
                    wincount += 1
                    if wincount == 4:
                        print(col, row, value)
                        return True, col, row, value
                elif col <= 2:
                    col = 0
                else:
                    wincount = 0
                    value = board[col][row]
            elif col <= 3:
                col = 0
            else:
                wincount = 0
                value = board[col][row]
            col -= 1
            row -= 1

    return False, 0, 0, 0

###############################################################################

print()
showIndicators()
showBoard(board)
#showColumns(columns)

while True:
    if player == -1:
        print("\n\n––––––\u001b[33;1m Gelb ist am Zug \u001b[0m––––––")
    elif player == 1:
        print("\n\n––––––\u001b[31;1m  Rot ist am Zug \u001b[0m––––––")

    readout = input("Bitte Spalte wählen (1,..,7): ")
    counter += 1
    print("counter",counter)
    #readout = str(randomMove(board, columns, player))
    print()

    if readout.isdigit():
        col = int(readout) - 1
        if (col <= 6 and col >= 0):

            player = placeCoin(board, col, player)
            showColumns(columns)

            #print("Vertical:", checkVertical(col))
            #print("Horizontal:", checkHorizontal(col))
            #print("RisingDiag:", checkRisingDiagonal(col))
            #print("FallingDiag:", checkFallingDiagonal(col))
            #print("Draw:", checkDraw(columns))
            #randomMove(board, columns, player)

            if checkVertical(board, col):
                print("Vertical")
                #if player == -1:
                #    print("\n\n\n>>>>>>\u001b[31;1m" +
                #          "  Rot  gewinnt!  " +
                #          "\u001b[0m<<<<<<\n\n\n")
                #else:
                #    print("\n\n\n>>>>>>\u001b[33;1m" +
                #          "  Gelb gewinnt!  " +
                #          "\u001b[0m<<<<<<\n\n\n")
                break

            if checkHorizontal(board, col):
                print("Horizontal")
                break

            if checkRisingDiagonal(board, col):
                print("Rising")
                break

            if checkFallingDiagonal(board, col):
                print("Falling")
                break

            if checkDraw(columns):
                print("\n\n\n–––––– Unentschieden! ––––––\n\n\n")
                break
    else:
        print("Ungültige Eingabe! (not an int)")
        #break

    print()

checkBoardRising(board)

