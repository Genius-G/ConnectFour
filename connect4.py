#!/usr/bin/python3

import random
import os
import numpy as np
from colorama import Fore, Back, Style
from Board import Board
from Minimax import Minimax


class Connect4:
    '''
    version 0.9 - 09.Juni 2020

    Der Code enthält bisher:
        Methoden für...
        ... eine Bildschirmausgabe
        ... das Platzieren eines Chips

    Es fehlen:
        Methoden für...
        ... das Evaluieren potentieller Spielzüge
        ... die Auswahl eines Spielzuges anhand vorheriger Evaluationen
        ... die Interaktion mit dem Roboter (wartet auf finales Design)
    '''

    # Constructor
    def __init__(self):
        self.gameboard = Board() # Gibt das Spielbrett
        self.player = random.choice([-1, 1])  # legt den Start Spieler fest {-1, 1}
        self.players = {-1:"Gelb", 1:"Rot"}
        self.counter = 0 # Anzahl der Spielzuege
        self.finished = False

    # Display functions –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    def showBoard(self):
        """ Zeigt das Spielbrett an für Ausgabe in der Kommandozeile """

        for i in range(6):
            printstring = ""
            for j in range(7):
                if self.gameboard.board[i][j] == 0:
                    printstring += " 0 "
                if self.gameboard.board[i][j] == 1:
                    # färbt die Chips rot 
                    printstring += "\u001b[41;1m\u001b[31m x \u001b[0m\u001b[0m"
                if self.gameboard.board[i][j] == -1:
                    # färbt die Chips gelb
                    printstring += "\u001b[43;1m\u001b[33m o \u001b[0m\u001b[0m"

            print(printstring)

    def showIndicators(self):
        """ Zeigt die Indikatoren an für Ausgabe in der Kommandozeile """
        print("_1__2__3__4__5__6__7_")

    def showTurnOrder(self):
        """ Zeige welcher Spieler an der Reihe ist """ 

        if self.player == -1:
            print("\n––––––\u001b[33;1m Gelb ist am Zug \u001b[0m––––––")
        elif self.player == 1:
            print("\n––––––\u001b[31;1m Rot ist am Zug \u001b[0m––––––")
                        
        # Gebe aktuellen Spielzug aus
        print("Spielzug: ", self.counter)

    def readInputFromConsole(self):
        # Lese Input aus der Kommandozeile ein
        readout = input("Bitte Spalte wählen (1,..,7): ")

        # Überprüfe auf (int)
        if readout.isdigit():
            # Verschiebe aus Bedienungsgründen um 1 
            col = int(readout) - 1

            # Überprüfe auf col in {1, ..., 6}
            if (col >= 0 and col <= 6):
                return col

            # Falls die Eingabe nicht in {1, ..., 6} liegt
            else:
                print()
                self.clearScreen()
                self.showIndicators()
                self.showBoard()
                print("Ungültige Eingabe! (nicht in {1, ..., 6})")

        
        # Falls abgebrochen werden soll
        elif (readout == 'q' or readout == 'quit'):
            self.finished = True
        
        # Falls die Eingabe kein Integer ist
        else:
            print()
            self.clearScreen()
            self.showIndicators()
            self.showBoard()
            print("Ungültige Eingabe! (Kein Integer)")

    def showEndOfGame(self):
        # Überprüfe auf Gewinner 
        if self.gameboard.checkForWinner():
            print("\n–––––– {} hat gewonnen! ––––––\n".format(self.players[self.player]))

        # Überprüfe aus Unentschieden
        elif self.gameboard.checkForDraw():
            print("\n–––––– Unentschieden! ––––––\n")

    def clearScreen(self):
        """ Löscht die Ausgabe in der Kommandozeile """
        os.system('cls' if os.name=='nt' else 'clear')

    # AI stuff ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    def randomMove(self):
        """ returns a random move from possible moves between {1, ..., 7} """
        return random.choice(self.gameboard.selectableColumns()) + 1

    def calculateResponses(self, difficulty):
        """ look ahead with minimax """
        mini = Minimax(self.gameboard)
        return mini.bestMove(difficulty, self.player)

    # Game functions ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––--
    def enterPiece(self, player, col):
        """ enters the Piece at col for player """
        self.counter += 1
        self.gameboard.enterPiece(player, col)

    def passTurn(self):
        """ passes the turn and changes the current player """
        self.player *= -1
    
    def main(self):
        """ This is demonstration on the console """
        print()
        self.showIndicators()
        self.showBoard()
        
        # Game Loop
        while True:

            # Zeige welche Farbe am Zug ist
            self.showTurnOrder()
            
            col = -1
            # Testing AI
            if self.player == 1:
                #col = self.randomMove()
                col = self.readInputFromConsole()
                print(col)
            else:
                # Lese Input aus der Kommandozeile ein
                col = self.calculateResponses(5)

            # Überprüfe, ob Spielzug möglich ist
            if True:

                # Werfe einen Chip ein
                self.gameboard.enterPiece(self.player, col)

                # Erhöhe Spielzug um eins
                self.counter += 1

                # Lösche die Ausgabe auf der Konsole
                self.clearScreen()

                # Gebe die Änderung aus
                self.showIndicators()
                self.showBoard()
                print()

                # Überprüfe auf Gewinner
                if self.gameboard.checkForWinner():
                    self.finished = True 

                # Überprüfe auf ob Spiel beendet
                if self.finished:
                    self.showEndOfGame()
                    break

                # Spielerwechsel
                self.passTurn()

            else:
                print("Spalte {} ist schon voll".format(col))
            
# main Methode zum Ausführen bei Aufruf
if __name__ == "__main__": 
    game = Connect4()
    game.main()