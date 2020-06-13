#!/usr/bin/python3

from Robot import Robot
from Connect4 import Connect4

class LegoRobot():

    def __init__(self):
        self.robot = Robot()
        self.game = Connect4()

    def humanPlayersTurn(self, color):
        
        # überprüfe welche Farbe der menschliche Spieler hat
        if color == 'Rot':
            # hole einen roten Chip
            #self.robot.setRedColor()
            self.robot.getRedCoin()

        elif color == 'Gelb':
            # hole einen gelben Chips
            #self.robot.setYellowColor()
            self.robot.getYellowCoin()

        # Übergebe die Kontrolle dem menschlichen Spieler
        self.robot.manualControl()
        # Er bestätigt durch beide gleichzeitig

        # Zum Schluss wird der Coin eingeschmissen beim Roboter ...
        self.robot.releaseCoin()
        # ... und beim Game
        self.game.enterPiece(self.game.player, self.robot.currentPosition - 1)

    def robotPlayersTurn(self, color):
        # überprüfe welche Farbe der Roboter Spieler hat
        if color == 'Rot':
            # hole einen roten Chip
            #self.robot.setRedColor()
            self.robot.getRedCoin()

        elif color == 'Gelb':
            # hole einen gelben Chip
            #self.robot.setYellowColor()
            self.robot.getYellowCoin()

        # Übergebe die Kontrolle dem meschlichen Spieler
        self.robot.driveToColumn(self.game.calculateResponses(3))

        # Zum Schluss wird der Coin eingeschmissen beim Roboter ...
        self.robot.releaseCoin()
        # ... und beim Game
        self.game.enterPiece(self.game.player, self.robot.currentPosition)

    def play_Game(self):
        """ Diese Funktion ist der Ablauf des Lego Roboters.
            Der Lego Roboter ist aktiv bis ein Spiel beendet wurde.
            Darin spielt ein Mensch gegen den Roboter.
        """

        # Kalibrierung
        #self.robot.calibrate()

        # Game Loop
        while self.game.finished == False:

            # Der menschliche Spieler ist an der Reihe
            if self.game.player == 1:
                
                self.humanPlayersTurn(self.game.player_color)

            # Der Roboter ist an der Reihe
            else:
                self.robotPlayersTurn(self.game.player_color)
                
            # Nachdem einer der beiden dran war, wird getauscht
            self.game.passTurn()

        # Wenn gewonnen wurde, dann eine coole Melodie spielen
        self.robot.playMusic()

    

if __name__ == "__main__": # Default "main method" idiom.
    LegoRobot = LegoRobot()
    LegoRobot.play_Game()
