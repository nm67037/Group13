import RPi.GPIO as GPIO
import math
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#setting up GPIO's of the raspberry pi
led = 6 #GPIO to Error Led
clk0 = 5 #GPIO to first display's dff's clock pin
clk1 = 7 #GPIO to second display's dff's clock pin
clk2 = 16#GPIO to third display's dff's clock pin
clk3 = 12#GPIO to fourth display's dff's clock pin
DP = 11  # D-flip-flop input: 4D, 4Q
A = 25 # input: D6, output: Q6
B = 8 # input: 5D, output: 5Q
C = 9 # input: 3D, output: 3Q
D = 23 # input: 2D, output: 2Q
E = 22 # input: 1D, output: 1Q
F = 10 # input: 7D, output: 7Q
G = 24 # input: 8D, output: 8Q
#GPIOs of the keypad, the rows of x will be outputs, and columns of y will be inputs
x1 = 2 
x2 = 3 
x3 = 4
x4 = 14

y1 = 15
y2 = 18
y3 = 17
y4 = 27

rows = [x1, x2, x3, x4]
columns = [y1, y2, y3, y4]
SSD_Pins = [ A, B, C, D, E, F, G]
clks = [clk0, clk1, clk2, clk3]

OPP = SSD_Pins 
OPP.append(clks)
OPP.append(led)
OPP.append(DP)
OPP.append(rows)

for j in range(len(OPP)): #defining gpios to dff as output
    print(OPP[j])
    GPIO.setup(OPP[j], GPIO.OUT,initial=GPIO.LOW)

for i in range(len(columns)): #defining y columns as input
    GPIO.setup(columns[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

dt = [0, 0, 0, 0, 0, 0, 0, 10]
cA = [1, 1, 1, 0, 1, 1, 1, 11]
cB = [0, 0, 1, 1, 1, 1, 1, 12]
cC = [1, 0, 0, 1, 1, 1, 0, 13]
cD = [0, 1, 1, 1, 1, 0, 1, 14]
N1 = [0, 1, 1, 0, 0, 0, 0, 1]
N2 = [1, 1, 0, 1, 1, 0, 1, 2]
N3 = [1, 1, 1, 1, 0, 0, 1, 3]
N4 = [0, 1, 1, 0, 0, 1, 1, 4]
N5 = [1, 0, 1, 1, 0, 1, 1, 5]
N6 = [1, 0, 1, 1, 1, 1, 1, 6]
N7 = [1, 1, 1, 0, 0, 0, 0, 7]
N8 = [1, 1, 1, 1, 1, 1, 1, 8]
N9 = [1, 1, 1, 0, 0, 1, 1, 9]
N0 = [1, 1, 1, 1, 1, 1, 0, 0]
hsh = [0, 0, 0, 0, 0, 0, 0, 15]

numbers = [N0, N1, N2, N3, N4, N5, N6, N7, N8, N9]
row1_chars = [N1,N2,N3,cA]
row2_chars = [N4,N5,N6,cB]
row3_chars = [N7,N8,N9,cC]
row4_chars = [dt, N0, hsh, cD]
characters = [row1_chars, row2_chars, row3_chars, row4_chars]

global cmode,ssdstate,now,display,dspsel,flstime,dstate,diff,flashd,mminute,mhour,mset,b_press_count
cmode = 0
ssdstate = 1
dspel = 0
flstime = datetime.now()
dstate = True
diff = 0
flashd = 0
mminute = 0
mhour = 0
mset = 0
b_press_count = 0 #creating a global counting variable to keep track of how many times b is pressed. Initializing it at 0.

def readkeypad(): #this function needs to be told what row number it's looking at and what the characters in that row are
    global now, ssdstate, b_press_count, diff, flashd, mset
    outval = None
    while outval == None:
        for j in range(len(rows)) and range(len(characters)):
            GPIO.output(rows[j], GPIO.HIGH) 

            for i in range(len(columns)): #using iteration, check each column for logic HIGH
                if GPIO.input(columns[i]) == 1:
                    outval = characters[j][i] #column n is associated with character n in char array from function input
                    delay(0.35)
                    break

            GPIO.output(rows[j], GPIO.LOW) #resetting the row to go back to basic off state
        if outval is not None:
            print(f"Button pressed: {outval[7]}")
            if outval == cB:
                if cmode != 0:
                    b_press_count +=1
                    print(f"B pressed {b_press_count} times")
            
                    if b_press_count ==3:
                        print(f"Back to start mode!")
                        b_press_count = 0
                        startmode()
            if outval != cB:
                b_press_count = 0

            if outval == cD:
                print(cmode)
                print(datetime.now().second)
                print(diff)
                   
        if cmode == 1:
            if (datetime.now().minute - now.minute) != 0 and ssdstate == 1:    
                automode()
        elif cmode == 2:
            if flashd < 4:
                flash(flashd)
            if mset == 1 and (datetime.now().minute - now.minute) != 0 and ssdstate == 1:
                now = datetime.now()
                manmode(True)

            pass

    return outval

def flash(dply):
    global flstime, display, dstate, diff
    now = datetime.now()
    diff = abs(now.microsecond - flstime.microsecond)
#    print(diff)
    if diff > 500000:
        flstime = datetime.now()
        if dstate:
            printssd(hsh,clks[dply])
#            print("off")
        else:
#            print("on")
            printssd(numbers[display[dply]],clks[dply])
        dstate = not(dstate)

def printssd(input,clock):
    for i in range(7):
        GPIO.output(SSD_Pins[i],input[i])
    GPIO.output(clock, GPIO.HIGH)
    delay(.001)
    GPIO.output(clock, GPIO.LOW)

def ssdoff():
    global ssdstate
    ssdstate = 0
    for i in range(4):
        printssd(hsh,clks[i])
    while readkeypad() != hsh:
        pass
    ssdstate = 1
    if cmode == 0:
        startmode()
    elif cmode == 1:
        automode()
    elif cmode == 2:
        manmode(False)

def PMdot(bol):
    global display
    if bol:
        GPIO.output(DP, 1)
        printssd(numbers[display[1]],clks[1])
        GPIO.output(DP,0)

def errLED(bol):
    if bol:
        GPIO.output(led,1)
    else:
        GPIO.output(led,0)

def delay(secs):
    poll = datetime.now()#will fail on the border of x:59 and x+1:00 
    starttime = poll.minute * 60 + poll.second + poll.microsecond/pow(10,6)
    timecheck = starttime
    while timecheck - starttime < secs:
        poll = datetime.now()
        timecheck = poll.minute * 60 + poll.second + poll.microsecond/pow(10,6)
    #print(f"time elapsed:  {timecheck - starttime}")

def startmode():
    global cmode, display, flashd, mset
    cmode = 0
    flashd = 0
    mset = 0
    display = [0,0,0,0]
    errLED(0)
    print("startmode")
    for i in range(4):
        printssd(N0,clks[i])
    modesel = readkeypad()
    if modesel == cA:
        print("auto mode")
        cmode = 1
        automode()
    elif modesel == cB:
        print("manual mode")
        cmode = 2
        manmode(False)
    elif modesel == hsh:
        print("display off/on")
        ssdoff()

def automode():
    global cmode, now, display
    now = datetime.now()
    hour = now.hour
    if now.hour > 12:
        hour -= 12
    #                   H1             H2               M1                  M2
    display = [math.floor(hour/10), hour%10, math.floor(now.minute/10) ,now.minute%10]
    for i in range(len(display)):
        printssd(numbers[display[i]],clks[i])
    if now.hour >= 12:
        PMdot(True)
    else:
        PMdot(False)
    while cmode == 1:
        if readkeypad() == hsh:
            ssdoff()
    

def manmode(update):
    global cmode, display, flashd, mhour, mminute, mset, now
    if not(mset):
        inv = True
        print("first display")
        while inv:#set first seven segment display
            input = readkeypad()
            if input[7] > 2:
                if input != cB:
                    errLED(1)
                print("Invalid input")
            else:
                display[0] = input[7]
                inv = False
                errLED(0)
        inv = True
        printssd(numbers[display[0]],clk0)
        flashd = 1
        print("second display")
        while inv:#set second seven segment display
            input = readkeypad()
            if display[0] == 2:
                if input[7] > 3:
                    if input != cB:
                        errLED(1)
                else:
                    display[1] = input[7]
                    inv = False
                    errLED(0)
            else:
                if input[7] > 9:
                    if input != cB:
                        errLED(1)
                else:
                    display[1] = input[7]
                    inv = False
                    errLED(0)
        inv = True
        printssd(numbers[display[1]],clk1)
        mhour = display[0] * 10 + display[1]
        hour = mhour
        if hour > 12:
            hour -= 12
            display = [math.floor(hour/10), hour%10, 0 , 0]
            printssd(numbers[display[0]],clk0)
            printssd(numbers[display[1]],clk1)
            PMdot(True)
        elif mhour == 12:
            PMdot(True)
        elif hour == 0:
            display = [1, 2, 0, 0]
        flashd = 2
        print("third display")
        while inv:
            input = readkeypad()
            if input[7] > 5:
                if input != cB:
                    errLED(1)
            else:
                display[2] = input[7]
                inv = False
                errLED(0)
        inv = True
        printssd(numbers[display[2]],clk2)
        flashd = 3
        print("fouth display")
        while inv:
            input = readkeypad()
            if input[7] > 9:
                if input != cB:
                    errLED(1)
            else:
                display[3] = input[7]
                inv = False
                errLED(0)
        printssd(numbers[display[3]],clk3)
        flashd = 4
        mminute = 10 * display[2] + display[3]
        mset = 1
        print("manual clock set")
        now = datetime.now()
    elif update:
        mminute += 1
        if mminute == 60:
            mminute = 0
            mhour += 1
        if mhour == 24:
            mhour = 0
    hour = mhour
    if hour > 12:
        hour -= 12
    elif hour == 0:
        hour = 12
    #                   H1             H2               M1                  M2
    display = [math.floor(hour/10), hour%10, math.floor(mminute/10) ,mminute%10]
    for i in range(len(display)):
        printssd(numbers[display[i]],clks[i])
    if mhour >= 12:
        PMdot(True)
    else:
        PMdot(False)    

    while cmode == 2:
        if readkeypad() == hsh:
            ssdoff()
running = True
while running:
    startmode()

