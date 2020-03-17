#!/usr/bin/env python3



from ev3dev.auto import *
import random

# Connect EV3 color and touch sensors to any sensor ports
c = ColorSensor()
t1 = TouchSensor('in1')
t2 = TouchSensor('in2')
m = LargeMotor('outA')
m2 = Motor('outB')
b= Button()

screen = Screen()
import ev3dev.fonts as fonts
# Put the color sensor into COL-COLOR mode.
c.mode = 'COL-COLOR'

def getChip(player):
    if player == 0:
        m.run_forever(speed_sp=1000)
        while True:
            if c.value()== 5:
                m.stop(stop_action="hold")
                time.sleep(3)
                break
        player += 1
        currPosition= 0
    elif player == 1:
        m.run_forever(speed_sp=-1000)
        while True:
            if c.value()== 5:
                m.stop(stop_action="hold")
                time.sleep(3)
                break
        player -=1
        currPosition = 8
    return currPosition,player



def selectPlace():
    print("selectPlace")
    zielspalte = 0 #Im Moment gewählte Spalte
    tStatus1 = 0 #0= nicht gedrueckt/ 1= gedrueckt
    tStatus2 = 0
    while t1.value()!=1 or t2.value()!=1:
        if tStatus1 != t1.value():
            tStatus1 = t1.value()
            zielspalte -= t1.value()
            print(zielspalte)
            if zielspalte <1:
                zielspalte = 1
        if tStatus2 != t2.value():
            tStatus2= t2.value()
            zielspalte +=t2.value()
            print(zielspalte)
            if zielspalte > 7:
                zielspalte = 7
                time.sleep(1)
        #TODO display on display
        #screen.draw.text((10, 10), zielspalte , font=fonts.load('luBS14'))
    return zielspalte


def gotoPosition(zielspalte,currPosition):
    print("gotoPosition")
    colorstatus = 0 #speichert temporar die Farbe
    bewegungscounter= zielspalte-currPosition #berechnet wie weit sich der Wagen bewegen muss
    print(bewegungscounter)

    if bewegungscounter <0:
        m.run_forever(speed_sp=200) #TODO schlecht, dass der Wagen erst loslaeuft und dann die Farbe checkt, besser glechzeitig/davor
        while bewegungscounter != 0:  # gehe zur gewählte Position
            if colorstatus != (c.color):
                if c.color == 1 or c.color == 6:
                    colorstatus = c.color
                    bewegungscounter += 1
                    print("Farbwechsel wurde erkannt und der Bewegungscounter um 1 erhoeht")
                    print("Bewegungscounter: ",bewegungscounter)
                    print("color: ",colorstatus)

    if bewegungscounter >0:
        m.run_forever(speed_sp=-200)
        while bewegungscounter != 0:  # gehe zur gewählte Position
            #if colorstatus == (c.color):
                #print("gleiche Farbe wurde erkannt")
            if colorstatus != (c.color):
                if c.color == 1 or c.color == 6:
                    colorstatus = c.color
                    bewegungscounter -= 1
                    print("Farbwechsel wurde erkannt und der Colorcounter um 1 verringert")
                    print("Bewegungscounter: ",bewegungscounter)
                    print("color: ",colorstatus)

        #TODO: maja diese zwei if-Bedingungen ähneln sich vom Code stark. Vielleicht lohnt sich dafür auch noch ne extra Funktion, allerdings wird mit dem Bewegungscounter anders umgegangen

    #wenn Zielposition erreicht wurde, lasse den Stein fallen
    m.stop(stop_action="hold")

    m2.run_timed(time_sp=500, speed_sp=-550)
    time.sleep(1)
    m2.run_timed(time_sp=500, speed_sp=550)
    time.sleep(1)



#def drivetoPosition():
    #TODO




'''DER ABLAUF:
1. get Chip() (rot oder gelb, je nach Zug & wer dran ist
2. select place() Auswahl der Position durch den Spieler bzw. Berechnung durch die KI
3. deliverchip() zur richtigen Position bringen

Die jeweilige Abläufe sollen an den Gegenspieler über das Display kommuniziert werden!
& es darf erst fertig sein, bis einer der beiden gewonnen hat
dann partymusik, wenn gewonnen wurde
'''


gewonnendefinition = False #check obs gewonnen hat, wird später von Silas? ausgetauscht
player = random.choice([0,1]) #wählt welcher Spieler anfängt
#Calibrierung
currPosition = 0

while gewonnendefinition == False: #nicht gewonnen TODO 
    print("getChip")
    print (player)
    currPosition,player = getChip(player)
    print(player)
    #VERSION 1: Wagen fährt zu vorher ausgewälte Spalte (notwendig auch für Zug des Roboters)
    gotoPosition(selectPlace(),currPosition)
    #VERSION 2: Wagen wird dynamisch an die gewünschte Spalte gefahren
    #drivetoPosition()





