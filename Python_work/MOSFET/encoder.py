import RPi.GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

clk = 6
dt = 5
sw = 16

GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)

lastClkState = GPIO.input(clk)

steps = 0
turns = 0

while True:
    clkState = GPIO.input(clk)
    dtState=GPIO.input(dt)
  	if clkState!=lastClkState:
    	    if dtState!=clkState:
	      print("Clockwise")
    	      steps+=1
        else:
	  print("Counter-clockwise")
          steps-=1
    lastClkState=clkState
    print(steps)
    #print("None")
