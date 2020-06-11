#!/usr/bin/python3

from . import Connect4
from . import Robot

class LegoRobot():

    def __init__(self):
        self.robot = Robot.Robot()
        self.game = Connect4.Connect4()

    def humanPlayersTurn(self):
        # hole einen roten Chip
        self.robot.getRedCoin()

        # Übergebe die Kontrolle dem menschlichen Spieler
        self.robot.manualControl()
        # Er bestätigt durch beide gleichzeitig

        # Zum Schluss wird der Coin eingeschmissen beim Roboter ...
        self.robot.releaseCoin()
        # ... und beim Game
        self.game.enterPiece(self.game.player, self.robot.currentPosition)

    def robotPlayersTurn(self):
        # hole einen gelben Chip
        self.robot.getYellowCoin()

        # Übergebe die Kontrolle dem meschlichen Spieler
        self.robot.driveToColumn(self.game.randomMove())

        # Zum Schluss wird der Coin eingeschmissen beim Roboter ...
        self.robot.releaseCoin()
        # ... und beim Game
        self.game.enterPiece(self.game.player, self.robot.currentPosition)

    def play_Game(self):
        """ Diese Funktion ist der Ablauf des Lego Roboters.
            Der Lego Roboter ist aktiv bis ein Spiel beendet wurde.
            Darin spielt ein Mensch gegen den Roboter.
        """

    

if __name__ == "__main__": # Default "main method" idiom.
    LegoRobot = LegoRobot()
    LegoRobot.play_Game()
