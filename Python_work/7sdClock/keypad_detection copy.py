import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 6
clk0 = 5
clk1 = 7
clk2 = 16
clk3 = 12
DP = 11  # D-flip-flop input: 4D, 4Q
A = 25 # input: D6, output: Q6
B = 8 # input: 5D, output: 5Q
C = 9 # input: 3D, output: 3Q
D = 23 # input: 2D, output: 2Q
E = 22 # input: 1D, output: 1Q
F = 10 # input: 7D, output: 7Q
G = 24 # input: 8D, output: 8Q

SSD_Pins = [DP, A, B, C, D, E, F, G]
clks = [clk0, clk1, clk2, clk3]
OPP= SSD_Pins 
OPP.append(clks)
OPP.append(led)


for j in range(len(OPP)): #defining gpios to dff as output
    print(OPP[j])
    GPIO.setup(OPP[j], GPIO.OUT,initial=GPIO.LOW)

x1 = 2 
x2 = 3 
x3 = 4
x4 = 14

y1 = 15
y2 = 18
y3 = 17
y4 = 27

cA = [1, 1, 1, 0, 1, 1, 1]
cB = [0, 0, 1, 1, 1, 1, 1]
cC = [1, 0, 0, 1, 1, 1, 0]
cD = [0, 1, 1, 1, 1, 0, 1]
N1 = [0, 1, 1, 0, 0, 0, 0]
N2 = [1, 1, 0, 1, 1, 0, 1]
N3 = [1, 1, 1, 1, 0, 0, 1]
N4 = [0, 1, 1, 0, 0, 1, 1]
N5 = [1, 0, 1, 1, 0, 1, 1]
N6 = [1, 0, 1, 1, 1, 1, 1]
N7 = [1, 1, 1, 0, 0, 0, 0]
N8 = [1, 1, 1, 1, 1, 1, 1]
N9 = [1, 1, 1, 0, 0, 1, 1]
N0 = [1, 1, 1, 1, 1, 1, 0]
hsh = [0, 0, 0, 0, 0, 0, 0]
global lastval, ssdstate
lastval = None
ssdstate = False
onval = 0
rows = [x1, x2, x3, x4]
columns = [y1, y2, y3, y4]
row1_chars = [N1,N2,N3,cA]
row2_chars = [N4,N5,N6,cB]
row3_chars = [N7,N8,N9,cC]
row4_chars = ['*', N0, hsh, cD]
# row1_chars = [1,2,3,'A']
# row2_chars = [4,5,6,'B']
# row3_chars = [7,8,9,'C']
# row4_chars = ['*', 0, '#', 'D']
#hashcount = 0
characters = [row1_chars, row2_chars, row3_chars, row4_chars]

for j in range(len(rows)): #defining x rows as output
    GPIO.setup(rows[j], GPIO.OUT)

for i in range(len(columns)): #defining y columns as input
    GPIO.setup(columns[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readkeypad(rownum,char): #this function needs to be told what row number it's looking at and what the characters in that row are
    global ssdstate,lastval
    GPIO.output(rownum, GPIO.HIGH) 
    outval = None
    for i in range(len(columns)): #using iteration, check each column for logic HIGH
        if GPIO.input(columns[i]) == 1:
            outval = char[i] #column n is associated with character n in char array from function input
            sleep(0.35)
            break

    GPIO.output(rownum, GPIO.LOW) #resetting the row to go back to basic off state
    if outval is not None:
        print(f"Button pressed: {outval}")
        if outval == hsh:
            ssdon()
        else:
            ssdstate = True
            printssd(outval,clks[1])
            lastval = outval
    return outval

def printssd(input,clock):
    for i in range(7):
        GPIO.output(SSD_Pins[i],input[i])
    GPIO.output(clock, GPIO.HIGH)
    sleep(.001)
    GPIO.output(clock, GPIO.LOW)

def ssdon():
    global lastval,ssdstate
    if ssdstate == True:
        ssdstate = False
        for i in range(4):
            printssd(hsh,clks[i])
    else:
        ssdstate = True
        for i in range(4):
            printssd(lastval,clks[i])

#now, we need to constantly poll the x outputs to see if any row was engaged. 
#when the Pi detects an engaged row, we can call the readkeypad function
#given the rownum argument and the character array inside that row.

running = True

while running:
    for i in range(4):
        printssd(hsh,clks[i])
    for j in range(len(rows)) and range(len(characters)):
            readkeypad(rows[j],characters[j])