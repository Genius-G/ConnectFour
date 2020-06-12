#!/usr/bin/python3

from  import Robot
from .Connect4 import Connect4

class LegoRobot():

    def __init__(self):
        self.robot = Robot()
        self.game = Connect4()

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

        # Game Loop
        while self.game.finished == False:

            # Der menschliche Spieler ist an der Reihe
            if self.game.player == 1:
                self.humanPlayersTurn()

            # Der Roboter ist an der Reihe
            else:
                self.robotPlayersTurn()
                
            # Nachdem einer der beiden dran war, wird getauscht
            self.game.passTurn()

        # Wenn gewonnen wurde, dann eine coole Melodie spielen
        self.robot.playMusic()

    

if __name__ == "__main__": # Default "main method" idiom.
    LegoRobot = LegoRobot()
    LegoRobot.play_Game()
