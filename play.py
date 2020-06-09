#!/usr/bin/python3

from Connect4 import *
from Robot import *

class LegoRobot():

    def __init__(self):
        self.robot = Robot()
        self.game = Connect4()

    def humanPlayersTurn(self):
            #get Coin (einmal rot und einmal gelb - immer abwechselnd)
            #wechselt den Spieler, zwar etwas unübersichtlicher, aber spart Coder, da die if-Bedigungen hier eh stehen. einfacher hier das scho
            self.robot.getRedCoin()

            # Version 3: Die Kontrolle, dass der Wagen dann richtig über der Spalte liegt hier beim Spieler
            self.robot.manualControl()

            # Zum Schluss wird der Coin eingeschmissen beim Roboter ...
            self.robot.deliverCoin()
            # ... und beim Game
            self.game.enterPiece(1, self.robot.getCurrentPosition())

    def robotPlayersTurn(self):
        pass

    def play_Game(self):

        # Game Loop
        while self.game.finished == False:

            # Der menschliche Spieler ist an der Reihe
            if self.game.player == 1:
                humanPlayersTurn()

            # Der Roboter ist an der Reihe
            else:
                robotPlayersTurn()
                
            # Nachdem einer der beiden dran war, wird getauscht
            self.game.passTurn()

        # TODO, wenn gewonnen wurde, dann eine coole Melodie spielen
        self.robot.playMusic()

if __name__ == "__main__": # Default "main method" idiom.
    LegoRobot = LegoRobot()
    LegoRobot.play_Game()
