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
# consolitdateing vaules to be easily accessed
rows = [x1, x2, x3, x4]
columns = [y1, y2, y3, y4]
SSD_Pins = [ A, B, C, D, E, F, G]
clks = [clk0, clk1, clk2, clk3]
#compiling list of output GPIOS to prepare for setup
OPP = SSD_Pins 
OPP.append(clks)
OPP.append(led)
OPP.append(DP)
OPP.append(rows)

for j in range(len(OPP)): #defining gpios as output
    print(OPP[j])
    GPIO.setup(OPP[j], GPIO.OUT,initial=GPIO.LOW)

for i in range(len(columns)): #defining y columns as input
    GPIO.setup(columns[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#list of characters printable on the seven segment displays
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
#Making it so that an interger can by quickly converted to a printable character on a seven segment display
numbers = [N0, N1, N2, N3, N4, N5, N6, N7, N8, N9]
#characterizing all possible inputs from the keypad
row1_chars = [N1,N2,N3,cA]
row2_chars = [N4,N5,N6,cB]
row3_chars = [N7,N8,N9,cC]
row4_chars = [dt, N0, hsh, cD]
characters = [row1_chars, row2_chars, row3_chars, row4_chars]
#list of global variables that will need to be referenced by the methods that need them and initializing them
global cmode,ssdstate,now,display,flstime,dstate,diff,flashd,mminute,mhour,mset,b_press_count
cmode = 0 #keep track of which mode the clock is in, [start] = 0, [auto] = 1, and [manual] = 2
ssdstate = 1 #keeps track of whether or not the clock displays are on or not
flstime = datetime.now() #used to determine the elapsed time since change the state of a flashing display
dstate = True #used by flash() to keep track of the on/off state of the flashing display
diff = 0 #used by flash() to calculate the elapsed time
flashd = 0 #uesd by flash() to keep track of which display is flashing
mminute = 0 #used by manual mode to keep track of the minutes it has
mhour = 0 #used by manual mode to keep track of the hours it has
mset = 0 #used by manual mode to keep track of whether or not it has been set or not
b_press_count = 0 #creating a global counting variable to keep track of how many times b is pressed. Initializing it at 0.

def readkeypad(): #When called this iterates through each key on the keypad until a key is pressed
    global now, ssdstate, b_press_count, diff, flashd, mset
    outval = None #Initializing the output of the method
    while outval == None:
        for j in range(len(rows)) and range(len(characters)): #set a high state on each row of the keypad at a time
            GPIO.output(rows[j], GPIO.HIGH) 
            #in each iteration,the columns are checked against the row that is high
            for i in range(len(columns)): 
                if GPIO.input(columns[i]) == 1: 
                    outval = characters[j][i] #When a high state is detected the outval is set by which row and column are are being checked
                    delay(0.35) #Delay for debounce on input
                    break

            GPIO.output(rows[j], GPIO.LOW) #resetting the row to go back to basic off state
        if outval is not None: #When an input is detected, it is put through some logic
            print(f"Button pressed: {outval[7]}")
            if outval == cB and cmode != 0: #when the input is 'B' and the clock is not on the start menu, it is tallied
                b_press_count +=1
                print(f"B pressed {b_press_count} times")
        
                if b_press_count ==3:# On the third 'B' return to the start menu
                    print(f"Back to start mode!")
                    b_press_count = 0
                    startmode()
            if outval != cB: #If the input is not 'B' restart the b count
                b_press_count = 0

            if outval == cD: # The D key is used for debugging
                print(cmode)
                print(datetime.now().second)
                print(diff)
        #As readkeypad is the mainloop of this program, every iteration is used to see if auto mode or manual mode need to be updated
        #This is where the timing of the clocks is done
        if cmode == 1: #the time the autoclock has is checked against the current time
            if (datetime.now().minute - now.minute) != 0:
                automode()#If there is a difference of more than 1 minute, the clock is updated to reflect the new time
        elif cmode == 2:#Manual mode is checked to be updated
            if flashd < 4:#if flash has a valid display number it will be used
                flash(flashd)
            if mset == 1 and (datetime.now().minute - now.minute) != 0:#check to see if Manual mode needs to be updated
                now = datetime.now()
                manmode(True)#True makes the manual clock update its values

            pass

    return outval
#the flash method is told which display to flash and from there it determines whether or not to change the state of the display based on elapsed time
def flash(dply): 
    global flstime, display, dstate, diff
    now = datetime.now() #takes the current time to compare against the inital flash time
    diff = abs(now.microsecond - flstime.microsecond)#The count of microsecond resets after evey second so the absolute difference is used
    if diff > 500000:#If half a second has elapsed change the state of the display
        flstime = datetime.now()#restart the count
        if dstate:
            printssd(hsh,clks[dply])# if on turn off
        else:
            printssd(numbers[display[dply]],clks[dply])# if off print the current value saved for that display
        dstate = not(dstate)# invert the state tracker

def printssd(input,clock):#Controls which segments are turned on or off on the specified display
    for i in range(7):#iterate through each segment and set them based on the character printssd is fed with
        GPIO.output(SSD_Pins[i],input[i])
    GPIO.output(clock, GPIO.HIGH)#flash the clock pin of the dff controlling the display
    delay(.001)
    GPIO.output(clock, GPIO.LOW)
#turns the displays off
def ssdoff():
    global ssdstate
    ssdstate = 0
    for i in range(4):#iterate through each display to turn all segments off
        printssd(hsh,clks[i])
    while readkeypad() != hsh:#holds the program here until hash is pressed again
        pass
    ssdstate = 1 #sets the display state tracker back to on and reprints the display based on the mode it was in
    if cmode == 0:
        startmode()
    elif cmode == 1:
        automode()
    elif cmode == 2:
        manmode(False)#This skips the update to the values in the manual clock
# If this method is called it will turn on the DP pin and flash the clock of the pm display with its saved value and turn off the DP pin
def PMdot():
    global display
    GPIO.output(DP, 1)
    printssd(numbers[display[1]],clks[1])
    GPIO.output(DP,0)
# Turns the Error LED on or off dependant on the bol value
def errLED(bol):
    if bol:
        GPIO.output(led,1)
    else:
        GPIO.output(led,0)
#Replacement for sleep, only really used for debounce and to make sure the dff have time to update
def delay(secs):
    poll = datetime.now()#will fail on the border of x:59 and x+1:00 but given how delay is used, it is an highly unlikely error
    starttime = poll.minute * 60 + poll.second + poll.microsecond/pow(10,6)#Tally up to find the exact second of the hour delay is called
    timecheck = starttime
    while timecheck - starttime < secs:#loop until the elapsed time is equal to or greater than the time given to the method
        poll = datetime.now()
        timecheck = poll.minute * 60 + poll.second + poll.microsecond/pow(10,6)
    #print(f"time elapsed:  {timecheck - starttime}")
#The first method called upon starting the program
def startmode():
    global cmode, display, flashd, mset
    cmode = 0 #make the current mode reflect that it is in [start]
    flashd = 0 #reset the count for the flashing display
    mset = 0 #reset the set tracker for [manual]
    display = [0,0,0,0] #save the display to show all zeros
    errLED(0) #turn off the error led
    print("startmode")
    for i in range(4):
        printssd(N0,clks[i]) #print all zeros on all displays
    modesel = readkeypad() #what for a mode to be selected on the keypad
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
    now = datetime.now() #find the current time
    hour = now.hour #get the hour and convert it to 12 hour time
    if now.hour > 12:
        hour -= 12
    #Do math to save to display all the values of the segments
    #                   H1             H2               M1                  M2
    display = [math.floor(hour/10), hour%10, math.floor(now.minute/10) ,now.minute%10]
    if ssdstate: #If the display is on print all the values found above
        for i in range(len(display)):
            printssd(numbers[display[i]],clks[i])
        if now.hour >= 12: #Determine if AM or PM
            PMdot()
    while cmode == 1 and ssdstate: #If the clock is on, hold the program here until it is either turned off or brought back to the start menu
        if readkeypad() == hsh:
            ssdoff()

def manmode(update):
    global cmode, display, flashd, mhour, mminute, mset, now
    if not(mset): #If the clock has not been set, go through the setup procedure
        inv = True
        print("first display")
        while inv:#set first seven segment display
            input = readkeypad()
            if input[7] > 2 and input != cB: #check if the input is valid for the left most H
                errLED(1)
                print("Invalid input")
            else:
                display[0] = input[7] #if valid save it
                inv = False
                errLED(0)
        inv = True
        printssd(numbers[display[0]],clk0) #print the valid inputted value
        flashd = 1 #increment the flashing display
        print("second display")
        while inv:#set second seven segment display
            input = readkeypad()
            if display[0] == 2: #Check to see if the input is valid for a 20th hour
                if input[7] > 3 and input != cB:
                    errLED(1)
                else:
                    display[1] = input[7] #save the value and leave the loop
                    inv = False
                    errLED(0)
            else:
                if input[7] > 9 and input != cB: #check to see if the input is valid
                    errLED(1)
                else:
                    display[1] = input[7]#save the value and leave the loop
                    inv = False
                    errLED(0)
        inv = True
        printssd(numbers[display[1]],clk1)
        mhour = display[0] * 10 + display[1] #get the manually set hour
        hour = mhour #start calculating the hour that will be displayed
        if hour > 12:
            hour -= 12
            display = [math.floor(hour/10), hour%10, 0 , 0]
            printssd(numbers[display[0]],clk0)
            printssd(numbers[display[1]],clk1)
            PMdot()
        elif mhour == 12: #for 12 PM
            PMdot()
        elif hour == 0: #for 12 AM
            display = [1, 2, 0, 0]
        flashd = 2
        print("third display")
        while inv:
            input = readkeypad()
            if input[7] > 5 and input != cB:
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
            if input[7] > 9 and input != cB:
                errLED(1)
            else:
                display[3] = input[7]
                inv = False
                errLED(0)
        printssd(numbers[display[3]],clk3)
        flashd = 4 #final increment of the flashing display
        mminute = 10 * display[2] + display[3] #get the manually set minute
        mset = 1 #clock is not set
        print("manual clock set")
        now = datetime.now()
    elif update: #if when the manual clock method is called It can be told to update its values
        mminute += 1
        if mminute == 60: #prevent impossible minutes
            mminute = 0
            mhour += 1
        if mhour == 24: #prevent impossible hours
            mhour = 0
    hour = mhour #recalculate the hour that is displayed
    if hour > 12:
        hour -= 12
    elif hour == 0:
        hour = 12
    #                   H1             H2               M1                  M2
    display = [math.floor(hour/10), hour%10, math.floor(mminute/10) ,mminute%10]
    if ssdstate: #If the display is on print the values saved in display
        for i in range(len(display)):
            printssd(numbers[display[i]],clks[i])
        if mhour >= 12:
            PMdot()   
    while cmode == 2 and ssdstate: #hold the program here until the clock is turned off or if the cmode is brought back to [start]
        if readkeypad() == hsh:
            ssdoff()
running = True
while running:#If an invalid input for mode selection is given, the program is held here
    startmode()

