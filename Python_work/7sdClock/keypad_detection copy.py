import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

clk = 23
DP = 7  # DP
C = 25 # C
D = 10 # D
E = 24 # E
G = 22 # G
F = 9  # F
A = 11 # A
B = 8  # B
DFF_Pins = [clk, DP, A, B, C, D, E, F, G]
for j in range(len(DFF_Pins)): #defining gpios to dff as output
    GPIO.setup(DFF_Pins[j], GPIO.OUT,initial=GPIO.LOW)

x1 = 2 
x2 = 3 
x3 = 4
x4 = 14

y1 = 15
y2 = 18
y3 = 27
y4 = 17

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
            printssd(outval)
            lastval = outval
    return outval

def printssd(input):
    for i in range(7):
        GPIO.output(DFF_Pins[i + 2],input[i])
    GPIO.output(clk, GPIO.HIGH)
    sleep(.001)
    GPIO.output(clk, GPIO.LOW)

def ssdon():
    global lastval,ssdstate
    if ssdstate == True:
        ssdstate = False
        printssd(hsh)
    else:
        ssdstate = True
        printssd(lastval)

#now, we need to constantly poll the x outputs to see if any row was engaged. 
#when the Pi detects an engaged row, we can call the readkeypad function
#given the rownum argument and the character array inside that row.

running = True

while running:
    for j in range(len(rows)) and range(len(characters)):
            readkeypad(rows[j],characters[j])