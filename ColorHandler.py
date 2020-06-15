#!/usr/bin/python3

from ev3dev.auto import *

class ColorHandler():

    def __init__(self):
        # Verbinde EV3 mit Farbsensor
        self.color_Sensor = ColorSensor()
        # Put the color sensor into REF-RAW (RGB-RAW before) mode.
        self.color_Sensor.mode = 'REF-RAW'

        # Lege Startwerte an:
        # In der momentanen Fassung des Roboters wird nur maxvalue gemessen.
        # boundary wird daher als maxvalue/2 gehandhabt; andere Konfigurationen
        # sind allerdings möglich
        self.maxvalue = 100
        self.boundary = 50
        #self.minvalue = 0
        self.valueNow = 100

        self.colorNow = 'White'
        self.colorBef = 'White'


    def calibrateBoundary(self):
        # Definiere eine Schwelle zwischen Schwarz und Weiß
        self.maxvalue = self.color_Sensor.reflected_light_intensity
        self.boundary = self.maxvalue / 2


    def getAvgIntensity(self):
        # Messe in kurzer Folge 4 Intensitätswerte und bilde über sie den
        # Durchschnitt
        intensity1 = self.color_Sensor.reflected_light_intensity
        intensity2 = self.color_Sensor.reflected_light_intensity
        intensity3 = self.color_Sensor.reflected_light_intensity
        intensity4 = self.color_Sensor.reflected_light_intensity
        avg = (intensity1 + intensity2 + intensity3 + intensity4) / 4
        # print('currColor:', intensity1, intensity2, intensity3, intensity4, avg)
        return avg


    def currentColor(self):
        # Messe die momente reflektierte Lichtintensität und ordne ihr eine
        # Farbe zu
        if self.getAvgIntensity() > self.boundary:
            return 'White'
        else:
            return 'Black'


    def colorChanged(self):
        # Prüfe, ob sich die Farbe seit dem letzten Aufruf
        # dieser Funktion geändert hat
        self.colorNow = self.currentColor()
        if self.colorBef != self.colorNow:
            print(self.colorBef,' → ',self.colorNow)
            self.colorBef = self.colorNow
            return True
        else:
            return False


    def BlackToWhite(self):
        # Prüfe, ob ein Übergang von Schwarz nach Weiß stattgefunden hat
        if self.colorChanged() and self.colorNow == 'White':
            print('Black → White !')
            return True
        else:
            return False


    def WhiteToBlack(self):
        # Prüfe, ob ein Übergang von Weiß nach Schwarz stattgefunden hat
        if self.colorChanged() and self.colorNow == 'Black':
            print('White → Black !')
            return True
        else:
            return False


# Unused ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

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

