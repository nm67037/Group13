import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

x1 = 2 
x2 = 3 
x3 = 4
x4 = 14

y1 = 15
y2 = 18
y3 = 27
y4 = 17

rows = [x1, x2, x3, x4]
columns = [y1, y2, y3, y4]
row1_chars = [1,2,3,'A']
row2_chars = [4,5,6,'B']
row3_chars = [7,8,9,'C']
row4_chars = ['*', 0, '#', 'D']

characters = [row1_chars, row2_chars, row3_chars, row4_chars]

for j in range(len(rows)): #defining x rows as output
    GPIO.setup(rows[j], GPIO.OUT)

for i in range(len(columns)): #defining y columns as input
    GPIO.setup(columns[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readkeypad(rownum,char): #this function needs to be told what row number it's looking at and what the characters in that row are
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
    
    return outval

#now, we need to constantly poll the x outputs to see if any row was engaged. 
#when the Pi detects an engaged row, we can call the readkeypad function
#given the rownum argument and the character array inside that row.

running = True

while running:
    for j in range(len(rows)) and range(len(characters)):
            readkeypad(rows[j],characters[j])