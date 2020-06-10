#!/usr/bin/python3

import random
import numpy as np
import ev3dev.fonts as fonts
from ev3dev.auto import *

from Board import Board
from Minimax import Minimax
from ConnectFour import *
import time


class Robot():
    """ Diese Klasse beschreibt die Möglichkeiten des Roboters.
        Er kann einen Wagen bewegen und dieser einen Chip loslassen.

    """
    def __init__(self):
        # Connect EV3 with motors
        self.move_wagon_Motor = LargeMotor('outA')
        self.chip_release_Motor = Motor('outB')

        # Connect EV3 with touch sensors and color sensor
        self.color_Sensor = ColorSensor()
        #Put the color sensor into COL-COLOR mode.
        self.color_Sensor.mode = 'COL-COLOR'
        self.colors = {'No Color':0, 'Black':1, 'White':6, 'Red':5}

        # Ein Berührungsensor zum Kalibrieren
        self.touch_Sensor_1 = TouchSensor('in1')

        # Nutze die Tasten des Brick zur Steuerung
        self.button = Button()
        self.screen = Screen()

        # Lege aktuelle Position mit Kallibrierung fest
        self.currentPossition = self.callibrate()
    
    def getRedCoin(self):
        """ Holt sich einen roten Chip """
        self.move_wagon_Motor.run_forever(speed_sp=1000)
        while True:
            # Halte an, wenn der Farbsensor Rot sieht
            if color_Sensor.value()== self.colors['Red']:
                self.move_wagon_Motor.stop(stop_action="hold")
                time.sleep(3)
                break

    def getYellowCoin(self):
        """ Holt sich einen gelben Chip """
        self.move_wagon_Motor.run_forever(speed_sp=-1000)
        while True:
            # Halte an, wenn der Farbsensor Rot sieht
            if color_Sensor.value()== self.colors['Red']:
                self.move_wagon_Motor.stop(stop_action="hold")
                time.sleep(3)
                break

    def updatePosition(self):
        """ Lege die aktuelle Position mittels des Farbsensors fest """
        # TODO Teste diese Implemtierung
        position = self.color_Sensor.value()
        self.currentPossition = position

    def releaseCoin(self): #laesst Spielstein los
        self.chip_release_Motor.run_timed(time_sp=500, speed_sp=-550)
        time.sleep(1)
        self.chip_release_Motor.run_timed(time_sp=500, speed_sp=550)
        time.sleep(1)

    def manualControl(self):
        ''' Wenn er den rechten Buttton des Bricks drückt, fährt der Wagen nach rechts und anders herum,
            anschließend fährt der Wagen zur Seite, bis zur roten Farbe, um einen neuen Stein zu holen'''
        
        # definiere Unterfunktionen
        def left3(state):
            if state:
                self.move_wagon_Motor.run_forever(speed_sp=-500)
            else:
                self.move_wagon_Motor.stop(stop_action="hold")
        def right3(state):
            if state:
                self.move_wagon_Motor.run_forever(speed_sp=500)
            else:
                self.move_wagon_Motor.stop(stop_action="hold")

        # belege Unterfunktionen auf die Button des Bricks
        self.button.on_left = left3
        self.button.on_right = right3

        # Beachte Button Input des Bricks bis Enter gedrückt wird.
        while not self.button.enter:
            # Verarbeite Input
            self.button.process()

    def calibrate(self):
        """ fährt so lange in eine Richtung bis ein Berührungsensor auslöst, 
        dann kalibriert er für die Farba Weiß 
        """
        self.move_wagon_Motor.run_forever(speed_sp=1000)
        # Versuche die ersten 10 Sekunden zu kalibrieren
        # time() liefert Zeit in Mikrosekunden seit Aufruf
        while time.time() * 1000 <= 10000:
            # Halte an, wenn der Berührungssensor aktiviert wird
            if self.touch_Sensor_1.value() == 1:
                self.move_wagon_Motor.stop(stop_action="hold")
                time.sleep(1)
                self.color_Sensor.calibrate_white()
                break
        return 0

    #--------------------------------------v Sophie v-------------------------------------------------------

    def display(self, currPosition):
        # TODO display on display
        # display()
        currPosition=9
        #self.screen.draw.text((10, 10), currPosition , font=fonts.load('luBS14'))

    def selectPlace(self):
        print("selectPlace")
        zielspalte = 0 # Im Moment gewählte Spalte
        tStatus1 = 0 # 0 = nicht gedrueckt/ 1 = gedrueckt
        tStatus2 = 0
        while self.touch_Sensor_1.value()!=1 or self.touch_Sensor_2.value()!=1:
            if tStatus1 != self.touch_Sensor_1.value():
                tStatus1 = self.touch_Sensor_1.value()
                zielspalte -= self.touch_Sensor_1.value()
                print(zielspalte)
                if zielspalte <1:
                    zielspalte = 1
            if tStatus2 != self.touch_Sensor_2.value():
                tStatus2= self.touch_Sensor_2.value()
                zielspalte +=t2.value()
                print(zielspalte)
                if zielspalte > 7:
                    zielspalte = 7
                    time.sleep(1)
            #TODO display on display
            #self.screen.draw.text((10, 10), zielspalte , font=fonts.load('luBS14'))
        return zielspalte

    def gotoPosition1(self, zielspalte, currPosition):
        print("gotoPosition")
        colorstatus = 0 #speichert temporar die Farbe
        if currPosition < zielspalte:
            self.move_wagon_Motor.run_forever(speed_sp=200) #TODO schlecht, dass der Wagen erst loslaeuft und dann die Farbe checkt, besser glechzeitig/davor
            while currPosition != zielspalte:  # gehe zur gewählte Position
                if colorstatus != (c.color):
                    if color_Sensor.color == 1 or color_Sensor.color == 6:
                        colorstatus = color_Sensor.color
                        currPosition += 1
                        print("Farbwechsel wurde erkannt und der current Position um 1 erhoeht")
                        print("current Position: ",currPosition)
                        print("color: ",colorstatus)
        if currPosition > zielspalte:
            self.move_wagon_Motor.run_forever(speed_sp=-200)
            while currPosition != zielspalte:  # gehe zur gewählte Position
                #if colorstatus == (c.color):
                    #print("gleiche Farbe wurde erkannt")
                if colorstatus != (c.color):
                    if color_Sensor.color == 1 or color_Sensor.color == 6:
                        colorstatus = color_Sensor.color
                        currPosition -= 1
                        print("Farbwechsel wurde erkannt und der current Position um 1 verringert")
                        print("current Position: ",currPosition)
                        print("color: ",colorstatus)

            #TODO: maja diese zwei if-Bedingungen ähneln sich vom Code stark. Vielleicht lohnt sich dafür auch noch ne extra Funktion, allerdings wird mit dem Bewegungscounter anders umgegangen

    def gotoPosition2(self, currPosition):
        zielspalte = currPosition
        colorstatus = self.color_Sensor.color

        def left2(state, zielspalte):
            if state:
                '''wenn gedrück, mach nichts'''
            else:
                '''wenn losgelassen'''
                zielspalte -=1
                if zielspalte < 1:
                    zielspalte = 1

        def right2(state, zielspalte):
            if state:
                '''wenn gedrück, mach nichts'''
            else:
                '''wenn losgelassen'''
                zielspalte += 1
                if zielspalte > 7:
                    zielspalte = 7

        self.button.on_left = left2
        self.button.on_right = right2

        while not self.button.enter:
            self.button.process(zielspalte)
            #TODO display die zielspalte!!
            if zielspalte < currPosition:
                #fahre nach links
                self.move_wagon_Motor.run_forever(speed_sp=-500)
                while not zielspalte == currPosition:
                    if colorstatus != color_Sensor.color:
                        colorstatus = color_Sensor.color
                        currPosition -=1
            if zielspalte > currPosition:
                #fahre nach rechts
                self.move_wagon_Motor.run_forever(speed_sp=500)
                while not zielspalte == currPosition:
                    if colorstatus != color_Sensor.color:
                        colorstatus = color_Sensor.color
                        currPosition +=1
            #halte an, wenn zielspalte und position übereinstimmen
            self.move_wagon_Motor.stop(stop_action="hold")

    def gotoPosition2mitDrucksensor(self, currPosition):
        zielspalte = 1 # kann Werte zwischen 1 und 7 annehmen = Anzahl der Spalten, default bei 1
        self.buttonStatus1 = False #Knöpfe (Tasten des Bricks) geben True oder False zurück default auf false eingestellt
        self.buttonStatus2 = False
        while not self.button.enter: #Position ist erst fest, wenn enter gedrückt wurde
            if self.buttonStatus1 != self.button.right:
                self.buttonStatus1 = self.button.right
                if self.button.right == True:
                    zielspalte -= 1 #soll sich allerdings nur verändern, wenn Knopf gedrückt ist
                    print("Gewaehlte Spalte ist Nummer: ",zielspalte)
                if zielspalte < 1:
                    zielspalte = 1
                #move to Position
                if currPosition!= zielspalte: #TODO: cooler wäre es, wenn der Wagen sich bewegt und man glichzeitig die Position weiter bestimmen könnte.
                    colorstatus = color_Sensor.color
                    if currPosition < zielspalte:
                        self.move_wagon_Motor.run_forever(speed_sp=200)
                        if colorstatus != color_Sensor.color:
                            currPosition += 1
                    elif currPosition < zielspalte:
                        self.move_wagon_Motor.run_forever(speed_sp=-200)
                        if colorstatus != color_Sensor.color:
                            currPosition += 1
            if self.buttonStatus2 != self.button.left:
                self.buttonStatus2 = self.button.left
                if self.button.right == True:
                    zielspalte += 1  # soll sich allerdings nur verändern, wenn Knopf gedrückt ist
                    print("Gewaehlte Spalte ist Nummer: ", zielspalte)
                if zielspalte >7:
                    zielspalte = 7
                # move to Position
                if currPosition != zielspalte:  # TODO: cooler wäre es, wenn der Wagen sich bewegt und man gleichzeitig die Position weiter bestimmen könnte.
                    colorstatus = color_Sensor.color
                    if currPosition < zielspalte:
                        self.move_wagon_Motor.run_forever(speed_sp=200)
                        if colorstatus != color_Sensor.color:
                            currPosition += 1
                    elif currPosition < zielspalte:
                        self.move_wagon_Motor.run_forever(speed_sp=-200)
                        if colorstatus != color_Sensor.color:
                            currPosition += 1
                         
    # Manuelles Fahren mit Buttons auf Brick                        
    def gotoPosition3(self):

        def left3(state):
            if state:
                self.move_wagon_Motor.run_forever(speed_sp=-500)
            else:
                self.move_wagon_Motor.stop(stop_action="hold")
        def right3(state):
            if state:
                self.move_wagon_Motor.run_forever(speed_sp=500)
            else:
                self.move_wagon_Motor.stop(stop_action="hold")

        self.button.on_left = left3
        self.button.on_right = right3

        while not self.button.enter:  # This loop checks buttons state continuously, solange
            self.button.process() # calls appropriate event handlers

    def driveToPositionX(self, currPosition):
        zielspalte = 1 # kann Werte zwischen 1 und 7 annehmen = Anzahl der Spalten, default bei 1
        self.buttonStatus1 = False # Knöpfe (Tasten des Bricks) geben True oder False zurück default auf false eingestellt
        self.buttonStatus2 = False
        while not self.button.enter: # Position ist erst fest, wenn enter gedrückt wurde
            while self.buttonStatus1 == self.button.right:
                # fahre nach rechts
                self.move_wagon_Motor.run
                self.buttonStatus1 = self.button.right
                if self.button.right == True:
                    zielspalte -= 1 # soll sich allerdings nur verändern, wenn Knopf gedrückt ist
                    print("Gewaehlte Spalte ist Nummer: ",zielspalte)
                if zielspalte < 1:
                    zielspalte = 1
                # move to Position
                if currPosition!= zielspalte: # TODO: cooler wäre es, wenn der Wagen sich bewegt und man glichzeitig die Position weiter bestimmen könnte.
                    colorstatus = color_Sensor.color
                    if currPosition < zielspalte:
                        self.move_wagon_Motor.run_forever(speed_sp=200)
                        if colorstatus != color_Sensor.color:
                            currPosition += 1
                    elif currPosition < zielspalte:
                        self.move_wagon_Motor.run_forever(speed_sp=-200)
                        if colorstatus != color_Sensor.color:
                            currPosition += 1
            if self.buttonStatus2 != self.button.left:
                self.buttonStatus2 = self.button.left
                if self.button.right == True:
                    zielspalte += 1  # soll sich allerdings nur verändern, wenn Knopf gedrückt ist
                    print("Gewaehlte Spalte ist Nummer: ", zielspalte)
                if zielspalte >7:
                    zielspalte = 7
                # move to Position
                if currPosition != zielspalte:  # TODO: cooler wäre es, wenn der Wagen sich bewegt und man gleichzeitig die Position weiter bestimmen könnte.
                    colorstatus = color_Sensor.color
                    if currPosition < zielspalte:
                        self.move_wagon_Motor.run_forever(speed_sp=200)
                        if colorstatus != color_Sensor.color:
                            currPosition += 1
                    elif currPosition < zielspalte:
                        self.move_wagon_Motor.run_forever(speed_sp=-200)
                        if colorstatus != color_Sensor.color:
                            currPosition += 1
        releaseCoin()
    
    def playMusic(self):
        # TODO Coole Musik abspielen
        pass
