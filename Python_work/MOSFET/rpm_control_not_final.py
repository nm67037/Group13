import RPi.GPIO as GPIO
import time, tty, sys, termios
import sys
import pigpio, os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

clk = 6
dt = 5
sw = 16
pin = 19

GPIO.setup(clk,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw,GPIO.IN,pull_up_down=GPIO.PUD_UP)

os.system('clear')
pi =pigpio.pi()

lastClkState = GPIO.input(clk)
lastDtState = GPIO.input(dt)

debouncedClk = 1
debouncedDt = 0
steps = 0
turns = 0
delay = .001
turns = 0
duty = 0
frequency = 0
x = 0

startTime = time.perf_counter()
endTime = 0
elapsedTime = 0
totalTurns = 0




global state
state = 0

def changePWM():
    pi.hardware_PWM(pin,frequency,duty*10000)
def hardwarestate():
    global state
    if state == 0:
        state = 1
        changePWM()
    elif state == 1:
        state = 0
        pi.hardware_PWM(pin,0,0)


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
        
    endTime = time.perf_counter()
    elapsedTime = endTime - startTime
    if ((elapsedTime) > 1):
        print("Turns/sec = ", totalTurns)
        totalTurns = 0
        startTime = time.perf_counter()
    
    lastClkState = debouncedClk
    lastDtState = debouncedDt
    
    # Start of motor control code
    
    if state == 0:
        print(f"Frequency: {frequency}| Dutycycle: {duty}%| OFF")
    elif state == 1:
        print(f"Frequency: {frequency}| Dutycycle: {duty}%| ON")
    print()
    print("Controls: | F: ON/OFF|")
    print("Q: +100 hz| W: +10 hz| E: +10% DC")
    print("A: -100 hz| S: -10 hz| D: -10% DC") 
    x=sys.stdin.read(1)[0]
    if x == "q":
        frequency += 100
    elif x == "w":
        frequency += 10
    elif x == "e":
        duty += 10
    elif x == "a":
        frequency -= 100
    elif x == "s":
        frequency -= 10
    elif x == "d":
        duty -= 10
    elif x == "f":
        hardwarestate()
    if frequency > 20000:
        frequency = 20000
    elif frequency < 0:
        frequency = 0
    if duty > 100:
        duty = 100
    elif duty < 0:
        duty = 0
    os.system('clear')
    if state == 1:
        changePWM()