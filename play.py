#!/usr/bin/python3

from Connect4 import *
from Robot import *

class LegoRobot():

    def __init__(self):
        self.robot = Robot()
        self.game = Connect4()

    def humanPlayersTurn(self):
        # hole einen roten Chip
        self.robot.getRedCoin()

        # Übergebe die Kontrolle dem meschlichen Spieler
        self.robot.manualControl()
        # Er bestätigt die Eingabe mit Enter

        # Zum Schluss wird der Coin eingeschmissen beim Roboter ...
        self.robot.releaseCoin()
        # ... und beim Game
        self.game.enterPiece(1, self.robot.getCurrentPosition())

    def robotPlayersTurn(self):
        # hole einen roten Chip
        self.robot.getYellowCoin()

        # TODO Der Rest der Stuerung 
        """ Darin wird die Funktion self.game.randomMove() verwendet zum Testen.
            diese gibt eine Zahl zwischen 1 und 7.
            Wenn der Minimax Algorithmus funktioniert nimmt man die Funktion
            self.game.calculateResponse() 
            diese gibt auch eine Zahl zwischen 1 und 7.
        """

    def play_Game(self):
        """ Diese Funktion ist der Ablauf des Lego Roboters.
            Der Lego Roboter ist aktiv bis ein Spiel beendet wurde.
            Darin spielt ein Mensch gegen den Roboter.
        """

        # Teste das ganze Projekt und ob es möglich ist das Ganze mit mehrern files zu machen
        self.robot.releaseCoin()

    

if __name__ == "__main__": # Default "main method" idiom.
    LegoRobot = LegoRobot()
    LegoRobot.play_Game()
