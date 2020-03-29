#!/usr/bin/env python3

from ev3dev.auto import *
import random

# Connect EV3 color and touch sensors to any sensor ports
m = LargeMotor('outA')
m2 = Motor('outB')
c = ColorSensor()
# Put the color sensor into COL-COLOR mode.
c.mode = 'COL-COLOR'
t1 = TouchSensor('in1')
t2 = TouchSensor('in2')
btn = Button()
screen = Screen()
import ev3dev.fonts as fonts


def getcoin(player):
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


def deliverCoin(): #laesst Spielstein los
    m2.run_timed(time_sp=500, speed_sp=-550)
    time.sleep(1)
    m2.run_timed(time_sp=500, speed_sp=550)
    time.sleep(1)


def display(currPosition):
    # TODO display on display
    # display()
    currPosition=9
    #screen.draw.text((10, 10), currPosition , font=fonts.load('luBS14'))




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


def gotoPosition1(zielspalte,currPosition):
    print("gotoPosition")
    colorstatus = 0 #speichert temporar die Farbe
    if currPosition < zielspalte:
        m.run_forever(speed_sp=200) #TODO schlecht, dass der Wagen erst loslaeuft und dann die Farbe checkt, besser glechzeitig/davor
        while currPosition != zielspalte:  # gehe zur gewählte Position
            if colorstatus != (c.color):
                if c.color == 1 or c.color == 6:
                    colorstatus = c.color
                    currPosition += 1
                    print("Farbwechsel wurde erkannt und der current Position um 1 erhoeht")
                    print("current Position: ",currPosition)
                    print("color: ",colorstatus)
    if currPosition > zielspalte:
        m.run_forever(speed_sp=-200)
        while currPosition != zielspalte:  # gehe zur gewählte Position
            #if colorstatus == (c.color):
                #print("gleiche Farbe wurde erkannt")
            if colorstatus != (c.color):
                if c.color == 1 or c.color == 6:
                    colorstatus = c.color
                    currPosition -= 1
                    print("Farbwechsel wurde erkannt und der current Position um 1 verringert")
                    print("current Position: ",currPosition)
                    print("color: ",colorstatus)

        #TODO: maja diese zwei if-Bedingungen ähneln sich vom Code stark. Vielleicht lohnt sich dafür auch noch ne extra Funktion, allerdings wird mit dem Bewegungscounter anders umgegangen


def gotoPosition2(currPosition):
    zielspalte= currPosition
    colorstatus= c.color

    def left2(state,zielspalte):
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

    btn.on_left = left2
    btn.on_right = right2

    while not btn.enter:
        btn.process(zielspalte)
        #TODO display die zielspalte!!
        if zielspalte<currPosition:
            #fahre nach links
            m.run_forever(speed_sp=-500)
            while not zielspalte == currPosition:
                if colorstatus != c.color:
                    colorstatus = c.color
                    currPosition -=1
        if zielspalte>currPosition:
            #fahre nach rechts
            m.run_forever(speed_sp=500)
            while not zielspalte == currPosition:
                if colorstatus != c.color:
                    colorstatus = c.color
                    currPosition +=1
        #halte an, wenn zielspalte und position übereinstimmen
        m.stop(stop_action="hold")



def gotoPosition2mitDrucksensor(currPosition):
    zielspalte = 1 # kann Werte zwischen 1 und 7 annehmen = Anzahl der Spalten, default bei 1
    btnStatus1 = False #Knöpfe (Tasten des Bricks) geben True oder False zurück default auf false eingestellt
    btnStatus2 = False
    while not btn.enter: #Position ist erst fest, wenn enter gedrückt wurde
        if btnStatus1 != btn.right:
            btnStatus1 = btn.right
            if btn.right == True:
                zielspalte -= 1 #soll sich allerdings nur verändern, wenn Knopf gedrückt ist
                print("Gewaehlte Spalte ist Nummer: ",zielspalte)
            if zielspalte < 1:
                zielspalte = 1
            #move to Position
            if currPosition!= zielspalte: #TODO: cooler wäre es, wenn der Wagen sich bewegt und man glichzeitig die Position weiter bestimmen könnte.
                colorstatus = c.color
                if currPosition < zielspalte:
                    m.run_forever(speed_sp=200)
                    if colorstatus != c.color:
                        currPosition += 1
                elif currPosition < zielspalte:
                    m.run_forever(speed_sp=-200)
                    if colorstatus != c.color:
                        currPosition += 1
        if btnStatus2 != btn.left:
            btnStatus2 = btn.left
            if btn.right == True:
                zielspalte += 1  # soll sich allerdings nur verändern, wenn Knopf gedrückt ist
                print("Gewaehlte Spalte ist Nummer: ", zielspalte)
            if zielspalte >7:
                zielspalte = 7
            # move to Position
            if currPosition != zielspalte:  # TODO: cooler wäre es, wenn der Wagen sich bewegt und man gleichzeitig die Position weiter bestimmen könnte.
                colorstatus = c.color
                if currPosition < zielspalte:
                    m.run_forever(speed_sp=200)
                    if colorstatus != c.color:
                        currPosition += 1
                elif currPosition < zielspalte:
                    m.run_forever(speed_sp=-200)
                    if colorstatus != c.color:
                        currPosition += 1


def gotoPosition3():

    def left3(state):
        if state:
            m.run_forever(speed_sp=-500)
        else:
            m.stop(stop_action="hold")
    def right3(state):
        if state:
            m.run_forever(speed_sp=500)
        else:
            m.stop(stop_action="hold")

    btn.on_left = left3
    btn.on_right = right3

    while not btn.enter:  # This loop checks buttons state continuously, solange
        btn.process() # calls appropriate event handlers



def drivetoPositionx(currPosition):
    zielspalte = 1 # kann Werte zwischen 1 und 7 annehmen = Anzahl der Spalten, default bei 1
    btnStatus1 = False #Knöpfe (Tasten des Bricks) geben True oder False zurück default auf false eingestellt
    btnStatus2 = False
    while not btn.enter: #Position ist erst fest, wenn enter gedrückt wurde
        while btnStatus1 == btn.right:
            #fahre nach rechts
            m.run
            btnStatus1 = btn.right
            if btn.right == True:
                zielspalte -= 1 #soll sich allerdings nur verändern, wenn Knopf gedrückt ist
                print("Gewaehlte Spalte ist Nummer: ",zielspalte)
            if zielspalte < 1:
                zielspalte = 1
            #move to Position
            if currPosition!= zielspalte: #TODO: cooler wäre es, wenn der Wagen sich bewegt und man glichzeitig die Position weiter bestimmen könnte.
                colorstatus = c.color
                if currPosition < zielspalte:
                    m.run_forever(speed_sp=200)
                    if colorstatus != c.color:
                        currPosition += 1
                elif currPosition < zielspalte:
                    m.run_forever(speed_sp=-200)
                    if colorstatus != c.color:
                        currPosition += 1
        if btnStatus2 != btn.left:
            btnStatus2 = btn.left
            if btn.right == True:
                zielspalte += 1  # soll sich allerdings nur verändern, wenn Knopf gedrückt ist
                print("Gewaehlte Spalte ist Nummer: ", zielspalte)
            if zielspalte >7:
                zielspalte = 7
            # move to Position
            if currPosition != zielspalte:  # TODO: cooler wäre es, wenn der Wagen sich bewegt und man gleichzeitig die Position weiter bestimmen könnte.
                colorstatus = c.color
                if currPosition < zielspalte:
                    m.run_forever(speed_sp=200)
                    if colorstatus != c.color:
                        currPosition += 1
                elif currPosition < zielspalte:
                    m.run_forever(speed_sp=-200)
                    if colorstatus != c.color:
                        currPosition += 1
    deliverCoin()



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

while gewonnendefinition == False: #nicht gewonnen TODO wird später von KI überprüft
    #get Coin (einmal rot und einmal gelb - immer abwechselnd)
    #wechselt den Spieler, zwar etwas unübersichtlicher, aber spart Coder, da die if-Bedigungen hier eh stehen. einfacher hier das scho
    currPosition,player = getcoin(player)


    #Jetzt sollen die Position gewählt werden und der Wagen dort hinfahren
    #VERSION 1: Wagen fährt zu vorher ausgewälte Spalte (notwendig auch für Zug des Roboters)
    gotoPosition1(selectPlace(),currPosition)

    #VERSION 2: Wagen wird dynamisch an die gewünschte Spalte gefahren
    '''dabei wird die Position jedesmal wieder geupdated (also mit der vom Spieler gewählte Zielspalte in Einklang gebracht),
     der Roboter weiß dabei immer auf welcher Position er sich befindet, da die Position mit dem Farbsensor bestimmt wird'''
    gotoPosition2(currPosition)

    #Version 3: Die Kontrolle, dass der Wagen dann richtig über der Spalte liegt hier beim Spieler
    '''wenn er den rechten Buttton des Bricks drückt, fährt der Wagen nach rechts und anders herum,
     anschließend fährt der Wagen zur Seite, bis zur roten Farbe, um einen neuen Stein zu holen'''
    gotoPosition3()
    #Zum Schluss wird der Coin eingeschmissen
    deliverCoin()

    #Die Schleife beginnt erneut, falls nicht gewonnen wurde


#TODO, wenn geonnen wurde, dann eine coole Melodie spielen