import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

clk = 6
dt = 5
sw = 16

GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw,GPIO.IN,pull_up_down=GPIO.PUD_UP)

lastClkState = GPIO.input(clk)
lastDtState = GPIO.input(dt)

debouncedClk = 1
debouncedDt = 0
steps = 0
turns = 0
delay = .001
turns = 0

startTime = time.perf_counter()
endTime = 0
elapsedTime = 0
totalTurns = 0


while True:
    
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    swState = GPIO.input(sw)
    
    if (swState == GPIO.LOW):
        print("Press")
        time.sleep(.5)
    
    if clkState != lastClkState:
        time.sleep(delay)
        clkState = GPIO.input(clk)
        if clkState != lastClkState:
            debouncedClk = clkState            
            
    if dtState != lastDtState:
        time.sleep(delay)
        dtState = GPIO.input(dt)
        if dtState != lastDtState:
            debouncedDt = dtState
    
    if debouncedClk != lastClkState:
        if debouncedDt != debouncedClk:
            steps += .5
            if ((steps % 1) == 0):
                print("Clockwise")
        else:
            steps -= .5
            if ((steps % 1) == 0):
                print("Counter-clockwise")
        if ((steps % 1) == 0):
            print(round(steps))
            totalTurns += 1
        time.sleep(delay)
        
        if (steps == 20):
            turns += 1
#     else:
        #print("None")
        
    endTime = time.perf_counter()
    elapsedTime = endTime - startTime
    if ((elapsedTime) > 1):
        print("Turns/sec = ", totalTurns)
        totalTurns = 0
        startTime = time.perf_counter()
    
    lastClkState = debouncedClk
    lastDtState = debouncedDt
    #print("None")
    #tps = float(turns) / seconds
    #print("turns/sec", tps)
    
    '''
    if clkState!=lastdtState:
        time.sleep(.005)
        clkState = GPIO.input(clk)
        if dtState!=clkState:
            time.sleep(.01)
            print("Clockwise")
            steps+=1
        else:
            time.sleep(.01)
            print("Counter-clockwise")
            steps-=1
    lastClkState=clkState
    '''
    
