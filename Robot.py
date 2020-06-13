#!/usr/bin/python3

from ev3dev.auto import *
import time

class Robot():
    """ Diese Klasse beschreibt die Möglichkeiten des Roboters.
        Er kann einen Wagen bewegen und dieser einen Chip loslassen.

    """
    # lege globale Variablen fest für die Bewegung des Wagens
    FAST_RIGHT = -1000
    SLOW_RIGHT = -200
    FAST_LEFT = 1000
    SLOW_LEFT = 200

    def __init__(self):
        # Verbinde EV3 mit Motoren
        self.move_wagon_Motor = LargeMotor('outA')
        self.chip_release_Motor = Motor('outB')

        # Verbinde EV3 mit Farbsensor
        self.color_Sensor = ColorSensor()
        # Put the color sensor into COL-COLOR mode.
        self.color_Sensor.mode = 'COL-COLOR'

        # Verbinde EV3 mit Tastsensoren
        self.left_touch_Sensor = TouchSensor('in1')
        self.right_touch_Sensor = TouchSensor('in2')
        self.calibrate_touch_Sensor = TouchSensor('in3')

        # Lege aktuelle Position ohne Kallibrierung fest
        # Für richtige Kalibrierung verwende calibrate()
        self.currentPosition = self.calibrate()
    
    def getRedCoin(self):
        """ Holt sich einen roten Chip """
        self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_LEFT)
        while True:
            # Halte an, wenn die aktuelle Position Null ist
            if self.currentPosition == 0 or self.calibrate_touch_Sensor.value():
                time.sleep(1)
                self.move_wagon_Motor.stop(stop_action="hold")
                time.sleep(3)
                break

            # halte aktuellen Farbwert fest
            colorstatus = self.color_Sensor.color()

            # wenn ein Farbwechsel statt findet, dann ...
            if colorstatus != self.color_Sensor.color():
                # ... veringere die aktuelle Position um eins
                self.currentPosition -= 1

    def getYellowCoin(self):
        """ Holt sich einen gelben Chip """
        self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_RIGHT)
        while True:
            # Halte an, wenn der die aktuelle Position Null ist
            if self.currentPosition == 8: # TODO TESTE OB DAS MIT 8 STIMMT
                time.sleep(1)
                self.move_wagon_Motor.stop(stop_action="hold")
                time.sleep(3)
                break

            # halte aktuellen Farbwert fest
            colorstatus = self.color_Sensor.color()

            # wenn ein Farbwechsel statt findet, dann ...
            if colorstatus != self.color_Sensor.color():
                # ... erhöhe die aktuelle Position um eins
                self.currentPosition += 1

    def releaseCoin(self):
        """ lässt den Spielstein los """
        self.chip_release_Motor.run_timed(time_sp=500, speed_sp=-550)
        time.sleep(1)
        self.chip_release_Motor.run_timed(time_sp=500, speed_sp=550)
        time.sleep(1)

    def manualControl(self):
        ''' lässt den Wagen links fahren, wenn linker Knopf gedrückt und
            lässt den Wagen rechts fahren, wenn rechter Knopf gedrückt und
            blaibt stehen, wenn beide gleichzeitig gedrückt werden.
        '''

        # führe die Schleife aus bis beide Knöpfe gleichzeitig gedrückt werden
        while not (self.left_touch_Sensor.value() and self.right_touch_Sensor.value()):
 
            # halte aktuellen Farbwert fest
            colorstatus = self.color_Sensor.color()

            # fahre nach links, wenn der linke Knopf gedrückt wird
            if self.left_touch_Sensor.value():
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_LEFT)

                # wenn ein Farbwechsel statt findet, dann ...
                if colorstatus != self.color_Sensor.color():
                    # ... veringere die aktuelle Position um eins
                    self.currentPosition -= 1

            # fahre nach rechts, wenn der rechte Knopf gedrückt wird      
            elif self.right_touch_Sensor.value():
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_RIGHT)

                # wenn ein Farbwechsel statt findet, dann ...
                if colorstatus != self.color_Sensor.color():
                    # ... erhöhe die aktuelle Position um eins
                    self.currentPosition += 1
            
            # Halte den Wagen an, wenn kein Knopf gedrückt wird
            else: 
                self.move_wagon_Motor.stop(stop_action="hold")

    def driveToColumn(self, destination):
        ''' fährt bis zur vorgegebenen Zielspalte und bleibt dann stehen.

        Args: destination [int] gibt die Zielspalte an
        '''
        while True:
            # halte aktuellen Farbwert fest
            colorstatus = self.color_Sensor.color()

            # fahre nach links, wenn das Ziel links von der aktuellen Position liegt
            if destination < self.currentPosition:
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_LEFT)

                # wenn ein Farbwechsel statt findet, dann ...
                if colorstatus != self.color_Sensor.color:
                    # ... veringere die aktuelle Position um eins
                    self.currentPosition -= 1

            # fahre nach rechts, wenn das Ziel rechts von der aktuellen Position liegt
            elif destination > self.currentPosition:
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_RIGHT)

                # wenn ein Farbwechsel statt findet, dann ...
                if colorstatus != self.color_Sensor.color:
                    # ... erhöhe die aktuelle Position um eins
                    self.currentPosition += 1
            
            # wenn angekommen am Ziel
            else:
                break # TODO TESTE OB ÜBER DEM RICHTIGEN SCHACHT

    def calibrate(self):
        """ fahre so lange in die Richtung des roten Spenders bis ein Berührungsensor auslöst
            oder nach 10 Sekunden, 
            dann kalibriert er für die Farba Weiß und legt die aktuelle Position auf 0.
        """
        self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_LEFT)
        # Versuche die ersten 10 Sekunden zu kalibrieren
        # time() liefert Zeit in Mikrosekunden seit Aufruf des Programms
        while time.time() * 1000 <= 10000: # TODO ÜBERPRÜFE OB 10 SEKUNDEN REICHEN

            # Halte an, wenn der Berührungssensor aktiviert wird
            if self.touch_Sensor_1.value():
                self.move_wagon_Motor.stop(stop_action="hold")
                time.sleep(1)
                self.color_Sensor.calibrate_white()
                break
        # Wenn der Wagen angehalten ist, kalibriere für die aktuelle Position
        self.currentPosition = 0
    
    def playMusic(self):
        # TODO Coole Musik abspielen
        pass
