#!/usr/bin/python3

from ev3dev.auto import *

class ColorHandler():

    def __init__(self):
        # Verbinde EV3 mit Farbsensor
        self.color_Sensor = ColorSensor()
        # Put the color sensor into REF-RAW (RGB-RAW before) mode.
        self.color_Sensor.mode = 'REF-RAW'

        #self.colors = {0:'Black', 1:'White'}

        self.maxvalue = 100
        self.boundary = 50
        #self.minvalue = 0
        self.valueNow = 100
        self.colorNow = 'White'
        self.colorBef = 'White'


    # Definiere eine Schwelle zwischen Schwarz und Weiß
    def calibrateBoundary(self):
        self.maxvalue = self.color_Sensor.reflected_light_intensity
        self.boundary = self.maxvalue / 2


    # Messe die momente reflektierte Lichtintensität und ordne ihr eine Farbe zu
    def currentColor(self):
        if self.color_Sensor.reflected_light_intensity > self.boundary:
            return 'White'
        else:
            return 'Black'


    # Prüfe, ob sich die Farbe seit dem letzten Aufruf
    # dieser Funktion geändert hat
    def colorChanged(self):
        self.colorNow = self.currentColor()
        if self.colorBef != self.colorNow:
            print(self.colorBef,' → ',self.colorNow)
            self.colorBef = self.colorNow
            return True
        else:
            return False


    # Prüfe, ob ein Übergang von Schwarz nach Weiß stattgefunden hat
    def BlackToWhite(self):
        if self.colorChanged() and self.colorNow == 'White':
            print('Black → White !')
            return True
        else:
            return False


    # Prüfe, ob ein Übergang von Weiß nach Schwarz stattgefunden hat
    def WhiteToBlack(self):
        if self.colorChanged() and self.colorNow == 'Black':
            print('White → Black !')
            return True
        else:
            return False


    def detectColorChange(self):
        """ bemerkt einen Farbwechsel von Hell und Dunkel
            gibt WAHR zurück, wenn ein Farbwechsel statt findet
        """

        # definiere Hilfsfunktion, um zu sagen, ob das aktuelle Feld ein
        # helles Feld ist.
        def _detectBrightColor():
            ''' gibt wahr zurück, wenn der Farbsensor hell sieht '''

            # überprüfe ob aktuelle Farbe heller als der kalibrierte Grenzwert
            if self.color_Sensor.reflected_light_intensity > self.boundary:

                # Gebe Wahr zurück, wenn das aktuelle Feld hell ist
                return True

            else:
                return False

        # lege 2 Mal die aktuelle Farbe fest
        color_one = _detectBrightColor()
        color_two = _detectBrightColor()
        #print("Die Helligkeit ist aktuell ", color_one, " und ", color_two)

        # überprüfe ob ein Unterschied zwischen den 2 Werten vor liegt
        if color_one != color_two:

            # gebe Wahr zurürck, da ein Farbwechsel statt gefunden hat
            return True

        else:
            # gebe Falsch zurück, da die Farben gleich sind
            return False

