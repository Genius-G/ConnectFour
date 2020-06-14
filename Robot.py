#!/usr/bin/python3

from ev3dev.auto import *
from ColorHandler import ColorHandler
import time

class Robot():

    FAST_RIGHT = 1000
    SLOW_RIGHT = 300
    VSLOW_RIGHT = 100
    FAST_LEFT = -1000
    SLOW_LEFT = -300
    VSLOW_LEFT = -100

    def __init__(self):
          # Verbinde EV3 mit Motoren
        self.move_wagon_Motor = LargeMotor('outA')
        self.chip_release_Motor = Motor('outB')

        # Nutze die LEDs
        self.leds = Leds()

        # Verbinde EV3 mit Tastsensoren
        self.left_touch_Sensor = TouchSensor('in1')
        self.right_touch_Sensor = TouchSensor('in2')
        self.calibration_touch_Sensor = TouchSensor('in3')

        # Verbinde EV3 mit Farbsensor
        self.ColorHandler = ColorHandler()

        # Lege einen Start-Wert für self.currentPosition fest
        self.currentPosition = 100

        # Legen einen Start-Wert für self.lastMovement fest
        self.lastMovement = 'Right'

        # Lege einen Start-Wert für self.colorstatus fest
        self.colorstatus = self.ColorHandler.currentColor()

        ''' Calibrate wird geändert '''
        # Lege aktuelle Position ohne Kallibrierung fest
        # Für richtige Kalibrierung verwende calibrate()
        #self.calibrate()


    def print_stats(self, row):
        print(row, self.colorstatus,
            self.ColorHandler.color_Sensor.reflected_light_intensity,
            self.ColorHandler.currentColor(), self.ColorHandler.boundary,
            self.currentPosition)



    def manualControl(self):
        ''' lässt den Wagen links fahren, wenn linker Knopf gedrückt und
            lässt den Wagen rechts fahren, wenn rechter Knopf gedrückt und
            bleibt stehen, wenn beide gleichzeitig gedrückt werden.
        '''

        # führe die Schleife aus bis beide Knöpfe gleichzeitig gedrückt werden
        while True:
            # halte aktuellen Farbwert fest
            self.colorstatus = self.ColorHandler.currentColor()

            if self.left_touch_Sensor.is_pressed and self.right_touch_Sensor.is_pressed:

                time.sleep(.5)
                if (self.left_touch_Sensor.is_pressed and self.right_touch_Sensor.is_pressed):
                    break

            # fahre nach links, wenn der linke Knopf gedrückt wird und sich
            # der Wagen nicht am Linken Rand befindet
            elif self.left_touch_Sensor.is_pressed and self.currentPosition != 0:
                '''das bedeutet nächstes Feld Schwarz -> Weiß'''
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_LEFT)

                # Falls sich der Wagen am Rand des Spielbretts befindet ...
                if self.currentPosition == 1 or self.currentPosition == 8:
                    if self.ColorHandler.BlackToWhite():
                        # Falls Übergang vermindere die Positionszahl
                        self.currentPosition -= 1
                        print('-1')
                        self.print_stats(85)

                # ... ansonsten ...
                elif self.ColorHandler.WhiteToBlack():
                    ''' Das wird durch WTB und BTW nicht mehr benötigt
                    # Teste, ob es sich dabei um eine Dopplung handelt ...
                    if self.lastMovement == 'Right':
                        # Falls ja, vermindere die Positionszahl NICHT und
                        # update die Richtungsvariable self.lastMovement
                        self.lastMovement = 'Left'
                        print('←←←Richtungswechsel←←←')
                        self.print_stats(80)
                    else:'''
                    # Falls Übergang vermindere die Positionszahl
                    self.currentPosition -= 1
                    print('-1')
                    self.print_stats(85)

            # fahre nach rechts, wenn der rechte Knopf gedrückt wird
            elif self.right_touch_Sensor.is_pressed and self.currentPosition != 8:
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_RIGHT)

                if self.currentPosition == 7 or self.currentPosition == 0:
                    if self.ColorHandler.WhiteToBlack():
                        # Falls Übergang vermindere die Positionszahl
                        self.currentPosition += 1
                        print('+1')

                # Falls ein Feldwechsel stattfindet ...
                elif self.ColorHandler.BlackToWhite():
                    '''
                    # Teste, ob es sich dabei um eine Dopplung handelt ...
                    if self.lastMovement == 'Left':
                        # Falls ja, erhöhe die Positionszahl NICHT und
                        # update die Richtungsvariable self.lastMovement
                        self.lastMovement = 'Right'
                        print('→→→Richtungswechsel→→→')
                        self.print_stats(99)
                    else:'''
                    # Falls nein, erhöhe die Positionszahl
                    self.currentPosition += 1
                    print('+1')
                    self.print_stats(104)

            # Halte den Wagen an, wenn kein Knopf gedrückt wird
            else:
                self.move_wagon_Motor.stop(stop_action="hold")


    def driveToColumn(self, destination):
        ''' fährt bis zur vorgegebenen Zielspalte und bleibt dann stehen.

        Args: destination [int] gibt die Zielspalte an und liegt im Bereich {0, ..., 8}
        '''

        #TODO Warum ist destionation zu klein??

        destination += 1


        # Überprüfe so lange bis man am Ziel ist
        while True:

            # fahre nach links, wenn das Ziel links von der aktuellen Position
            # liegt
            print('Ich bin bei ',self.currentPosition,' und möchte zu ',destination)
            if destination < self.currentPosition:
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_LEFT)

                # wenn ein Farbwechsel statt findet, dann ...
                if self.ColorHandler.BlackToWhite():
                    # ... veringere die aktuelle Position um eins, da der Wagen
                    # nach links fährt
                    self.currentPosition -= 1

            # fahre nach rechts, wenn das Ziel rechts von der aktuellen
            # Position liegt
            elif destination > self.currentPosition:
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_RIGHT)

                # wenn ein Farbwechsel statt findet, dann ...
                if self.ColorHandler.WhiteToBlack():
                    # ... erhöhe die aktuelle Position um eins, da der Wagen
                    # nach rechts fährt
                    self.currentPosition += 1
                    self.print_stats()

            # wenn angekommen am Ziel
            else:

                # TODO Korrektur von destination
                destination -= 1

                # halte den Wagen nach kurzen Verzögerung an
                #time.sleep(self.TIME_OFFSET)
                self.move_wagon_Motor.stop(stop_action="hold")
                # TODO TESTE OB ÜBER DEM RICHTIGEN SCHACHT
                break



    def releaseCoin(self):
        """ lässt den Spielstein los """

        # Halte zunächst den Wagen definitiv an
        self.move_wagon_Motor.stop(stop_action="hold")

        # Öffne den Schacht für 1 Sekunde
        self.chip_release_Motor.run_timed(time_sp=500, speed_sp=-550)
        time.sleep(1)
        self.chip_release_Motor.run_timed(time_sp=500, speed_sp=550)
        time.sleep(1)


    def getRedCoin(self):
        """ Holt sich einen roten Chip """
        self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_LEFT)
        while True:
            # Halte an, wenn die aktuelle Position Null ist
            if self.currentPosition == -1 or self.calibration_touch_Sensor.is_pressed:
                # Erhalte Roten Chip

                # Hold, lasse den Motor aber noch etwas Weiterfahren,
                # um unterschiede zwischen, Machanismus, Positionserkennung
                # und Kalibrierungsknopf
                time.sleep(.25)
                self.move_wagon_Motor.stop(stop_action="hold")

                # Kalibrierung
                # Dies ist nur auf der roten Seite möglich
                self.currentPosition = -1
                self.ColorHandler.calibrateBoundary()
                print('––––calibrateBoundary()')
                self.colorstatus = self.ColorHandler.currentColor()
                time.sleep(3)

                # Fahre auf das Spielbrett zu Position 1
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_RIGHT)

                # Ignoriere dabei den ersten Farbübergang ('White' -> 'Black'),
                # da er eine Dopplung von Position 0 darstellt
                while self.ColorHandler.WhiteToBlack() == False:
                    self.print_stats(134)
                print('–––––erstes Feld übersprungen')
                self.print_stats(136)

                while self.ColorHandler.BlackToWhite() == False:
                    self.print_stats(134)
                print('–––––zweites Feld übersprungen')
                self.print_stats(136)
                self.currentPosition += 1

                self.colorstatus = self.ColorHandler.currentColor()
                # Fahre weiter, Fahre weiter, bis der Übergang zu Position 1
                # ('Black' -> 'White') erkannt wird
                while self.ColorHandler.WhiteToBlack() == False:
                    self.print_stats(143)
                print('–––––in Position')
                self.print_stats(145)

                # Hold
                self.currentPosition += 1
                self.lastMovement = 'Right'
                print('GetRedCoin Position: ', self.currentPosition)
                self.move_wagon_Motor.stop(stop_action="hold")

                break

            # halte aktuellen Farbwert fest
            self.colorstatus = self.ColorHandler.currentColor()

            # wenn ein Farbwechsel statt findet, dann ...
            if self.currentPosition == 1 or self.currentPosition == 9:
                if self.ColorHandler.WhiteToBlack():
                    # ... veringere die aktuelle Position um eins
                    self.currentPosition -= 1
                    self.print_stats(160)
            else:
                if self.ColorHandler.BlackToWhite():
                    # ... veringere die aktuelle Position um eins
                    self.currentPosition -= 1
                    self.print_stats(160)

            self.print_stats(162)

    def getYellowCoin(self):
        """ Holt sich einen gelben Chip """
        self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_RIGHT)
        while True:
            # Halte an, wenn der die aktuelle Position Null ist
            if self.currentPosition == 9: # TODO TESTE OB DAS MIT 9 STIMMT
                time.sleep(.25)
                self.move_wagon_Motor.stop(stop_action="hold")

                # Kalibrierung
                # Dies ist nur auf der roten Seite möglich
                self.colorstatus = self.ColorHandler.currentColor()
                time.sleep(3)

                # Fahre auf das Spielbrett zu Position 1
                self.move_wagon_Motor.run_forever(speed_sp=self.VSLOW_LEFT)

                # Ignoriere dabei den ersten Farbübergang ('White' -> 'Black'),
                # da er eine Dopplung von Position 0 darstellt
                while self.ColorHandler.BlackToWhite() == False:
                    self.print_stats(274)
                print('–––––erstes Feld übersprungen')
                self.print_stats(276)

                while self.ColorHandler.WhiteToBlack() == False:
                    self.print_stats(279)
                print('–––––zweites Feld übersprungen')
                self.print_stats(281)
                self.currentPosition -= 1

                self.colorstatus = self.ColorHandler.currentColor()
                # Fahre weiter, Fahre weiter, bis der Übergang zu Position 1
                # ('Black' -> 'White') erkannt wird
                while self.ColorHandler.BlackToWhite() == False:
                    self.print_stats(288)
                print('–––––in Position')
                self.print_stats(290)

                # Hold
                self.currentPosition -= 1
                print('GetYellowCoin Position: ', self.currentPosition)
                self.lastMovement = 'Left'
                self.move_wagon_Motor.stop(stop_action="hold")

                break

            # halte aktuellen Farbwert fest
            self.colorstatus = self.ColorHandler.currentColor()

            # wenn ein Farbwechsel statt findet, dann ...
            if self.currentPosition == -1 or self.currentPosition == 7:
                if self.ColorHandler.BlackToWhite():
                    # ... veringere die aktuelle Position um eins
                    self.currentPosition += 1
                    self.print_stats(160)
            else:
                if self.ColorHandler.WhiteToBlack():
                    # ... veringere die aktuelle Position um eins
                    self.currentPosition += 1
                    self.print_stats(160)

            self.print_stats(162)
