#!/usr/bin/python3

from ev3dev.auto import *
import time

class Robot():
    """ Diese Klasse beschreibt die Möglichkeiten des Roboters.
        Er kann einen Wagen bewegen und dieser einen Chip loslassen.

    """
    # lege globale Variablen fest für die Bewegung des Wagens
    FAST_RIGHT = 1000
    SLOW_RIGHT = 300
    FAST_LEFT = -1000
    SLOW_LEFT = -300

    def __init__(self):
        # Verbinde EV3 mit Motoren
        self.move_wagon_Motor = LargeMotor('outA')
        self.chip_release_Motor = Motor('outB')

        # Verbinde EV3 mit Farbsensor
        self.color_Sensor = ColorSensor()
        # Put the color sensor into COL-REFLECT mode.
        self.color_Sensor.mode = 'REF-RAW'

        # Nutze die LEDs
        self.leds = Leds()

        # Verbinde EV3 mit Tastsensoren
        self.left_touch_Sensor = TouchSensor('in1')
        self.right_touch_Sensor = TouchSensor('in2')
        self.calibration_touch_Sensor = TouchSensor('in3')

        # Für richtige Kalibrierung verwende calibrate()
        self.currentPosition = self.calibrate()
        self.boundry = 500


    def print_stats(self):
        print('Aktuelle Position: ', self.currentPosition)

    def calibrate(self):
        """ fahre so lange in die Richtung des roten Spenders bis ein Berührungsensor auslöst
            oder nach 10 Sekunden, 
            dann kalibriert er für die Farba Weiß und legt die aktuelle Position auf 0.
        """
        self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_LEFT)
        
        # Kalibriere bis der Kalibrationssensor berührt wurde
        while True:

            # Halte an, wenn der Berührungssensor aktiviert wird
            if self.calibration_touch_Sensor.is_pressed:

                time.sleep(.5)
                self.move_wagon_Motor.stop(stop_action="hold")
                
                # Kalibriere den Wert fur die Grenze 
                # TODO TESTE OB DEINE IDEE KLAPPT MIT DEM TEILEN DURCH 2
                self.boundry = self.color_Sensor.reflected_light_intensity / 2
                
                break
        # Wenn der Wagen angehalten ist, kalibriere für die aktuelle Position
        self.move_wagon_Motor.stop(stop_action="hold")
        self.currentPosition = 0

    def detectColorChange(self):
        """ bemerkt einen Farbwechsel von Rot zu Weiß
            gibt WAHR zurück, wenn der Farbsensor Rot sieht    
        """

        # definiere Hilfsfunktion, um zu sagen, ob das aktuelle Feld ein helles Feld ist.
        def _detectBrightColor():

            # überprüfe ob aktuelle Farbe hell ist, oder nicht
            if self.color_Sensor.reflected_light_intensity > self.boundry:
                
                # Gebe Wahr zurück, wenn das aktuelle Feld hell ist
                return True

            else:
                return False

        # lege 2 Mal die aktuelle Farbe fest
        color_one = _detectBrightColor()
        color_two = _detectBrightColor()
        print("Die Helligkeit ist aktuell ", color_one, " und ", color_two)

        # überprüfe ob ein Unterschied zwischen den 2 Werten vor liegt
        if color_one != color_two:
            
            # gebe Wahr zurürck, da ein Farbwechsel statt gefunden hat
            return True

        else: 
            # gebe Falsch zurück, da die Farben gleich sind
            return False


    def getRedCoin(self):
        """ Holt sich einen roten Chip """
        self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_LEFT)
        while True:
            # Halte an, wenn die aktuelle Position Null ist oder der Kalibrationssensor berührt wurde
            if self.currentPosition == 0 or self.calibration_touch_Sensor.is_pressed:
                time.sleep(.1)
                self.move_wagon_Motor.stop(stop_action="hold")
                time.sleep(1)
                break

            

            # wenn ein Farbwechsel statt findet, dann ...
            if self.detectColorChange:
                # ... veringere die aktuelle Position um eins, da er nach links fährt
                self.currentPosition += -1
                self.print_stats()

    def getYellowCoin(self):
        """ Holt sich einen gelben Chip """
        self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_RIGHT)
        while True:
            # Halte an, wenn der die aktuelle Position Null ist
            if self.currentPosition == 8: # TODO TESTE OB DAS MIT 8 STIMMT
                time.sleep(.1)
                self.move_wagon_Motor.stop(stop_action="hold")
                time.sleep(1)
                break

            # wenn ein Farbwechsel statt findet, dann ...
            if self.detectColorChange():
                # ... erhöhe die aktuelle Position um eins, da er nach rechts fährt
                self.currentPosition += 1
                self.print_stats()

    def releaseCoin(self):
        """ lässt den Spielstein los """

        # Halte zunächst den Wagen an
        self.move_wagon_Motor.stop(stop_action="hold")

        # Öffne den Schacht für 1 Sekunde
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
        while not (self.left_touch_Sensor.is_pressed and self.right_touch_Sensor.is_pressed):

            # fahre nach links, wenn der linke Knopf gedrückt wird
            if self.left_touch_Sensor.is_pressed:
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_LEFT)

                # wenn ein Farbwechsel statt findet, dann ...
                if self.detectColorChange():
                    # ... veringere die aktuelle Position um eins, da der Wagen nach links fährt
                    self.currentPosition += -1
                    self.print_stats()

            # fahre nach rechts, wenn der rechte Knopf gedrückt wird      
            elif self.right_touch_Sensor.is_pressed:
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_RIGHT)

                # wenn ein Farbwechsel statt findet, dann ...
                if self.detectColorChange():
                    # ... erhöhe die aktuelle Position um eins, da der Wagen nach rechts fährt
                    self.currentPosition += 1
                    self.print_stats()
            
            # Halte den Wagen an, wenn kein Knopf gedrückt wird
            else: 
                self.move_wagon_Motor.stop(stop_action="hold")

    def driveToColumn(self, destination):
        ''' fährt bis zur vorgegebenen Zielspalte und bleibt dann stehen.

        Args: destination [int] gibt die Zielspalte an und liegt im Bereich {0, ..., 8}
        '''

        # Überprüfe so lange bis man am Ziel ist
        while True:

            # fahre nach links, wenn das Ziel links von der aktuellen Position liegt
            if destination < self.currentPosition:
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_LEFT)

                # wenn ein Farbwechsel statt findet, dann ...
                if self.detectColorChange():
                    # ... veringere die aktuelle Position um eins, da der Wagen nach links fährt
                    self.currentPosition += -1
                    self.print_stats()

            # fahre nach rechts, wenn das Ziel rechts von der aktuellen Position liegt
            elif destination > self.currentPosition:
                self.move_wagon_Motor.run_forever(speed_sp=self.SLOW_RIGHT)

                # wenn ein Farbwechsel statt findet, dann ...
                if self.detectColorChange():
                    # ... erhöhe die aktuelle Position um eins, da der Wagen nach rechts fährt
                    self.currentPosition += 1
                    self.print_stats()
            
            # wenn angekommen am Ziel
            else:
                
                # halte den Wagen an
                self.move_wagon_Motor.stop(stop_action="hold")
                # TODO TESTE OB ÜBER DEM RICHTIGEN SCHACHT
                break 


    def setRedColor(self):
        self.leds.set_color("LEFT", "RED")
        self.leds.set_color("RIGHT", "RED")

    def setYellowColor(self):
        self.leds.set_color("LEFT", "YELLOW")
        self.leds.set_color("RIGHT", "YELLOW")
    
    def playMusic(self):
        # TODO Coole Musik abspielen
        pass