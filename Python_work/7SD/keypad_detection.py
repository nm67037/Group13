import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

x1 = 1 #need to edit these values to the
x2 = 2 #actual GPIO pins. These numbers are placeholders
x3 = 3
x4 = 4

y1 = 5
y2 = 6
y3 = 7
y4 = 8

GPIO.setup(x1, GPIO.OUT) #all the x (rows) are considered outputs to the Pi
GPIO.setup(x2, GPIO.OUT)
GPIO.setup(x3, GPIO.OUT)
GPIO.setup(x4, GPIO.OUT)

GPIO.setup(y1, GPIO.IN) #all the y (columns) are considered inputs to the Pi
GPIO.setup(y2, GPIO.IN)
GPIO.setup(y3, GPIO.IN)
GPIO.setup(y4, GPIO.IN)

def readkeypad(rownum,char): #this function needs to be told what row number it's looking at and what the characters in that row are
    GPIO.output(rownum, GPIO.HIGH) 

    columns = [y1, y2, y3, y4]
    outval = None

    for i in range(len(columns)): #using iteration, check each column for logic HIGH
        if GPIO.input(columns[i]) == 1:
            outval = char[i] #column n is associated with character n in char array from function input
            break

    GPIO.output(rownum, GPIO.LOW) #resetting the row to go back to basic off state
    if outval is not None:
        print(f"Button pressed: {outval}")
    
    return outval

#now, we need to constantly poll the x outputs to see if any row was engaged. 
#when the Pi detects an engaged row, we can call the readkeypad function
#given the rownum argument and the character array inside that row.

running = True
rows = [x1, x2, x3, x4]
while running:
    for j in range(len(rows)):
        if GPIO.output(rows[j]) == 1:
            readkeypad(rows[j], [1,2,3,'A']) #I need to change the character array to include all character arrays, not just the first one
            break
        