import RPi.GPIO as GPIO
import time

import tty, sys, termios
import pigpio
import os
from time import sleep
os.system('clear')
filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)
pi =pigpio.pi()
pin = 19
duty = 0
frequency = 0
x = 0
global state
state = 0

# GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

clk = 22
dt = 27
sw = 17

GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize states and variables
lastClkState = GPIO.input(clk)
lastDtState = GPIO.input(dt)

debouncedClk = 1
debouncedDt = 0
steps = 0
turns = 0
delay = 0.001
turns = 0
my_variable = 0  # Variable to update with each step

startTime = time.perf_counter()
endTime = 0
elapsedTime = 0
totalTurns = 0

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


try:
    while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        swState = GPIO.input(sw)
        
        if swState == GPIO.LOW:
            print("Button Pressed")
            time.sleep(0.5)
            if state == 0:
                state = 1
            else:
                state =0
            print(state)
            

        
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
                steps += 0.5
                if (steps % 1) == 0:
                    print("Clockwise")
                    my_variable += 25  # Add 25 for each clockwise step
            else:
                steps -= 0.5
                if (steps % 1) == 0:
                    print("Counter-clockwise")
                    my_variable -= 25  # Subtract 25 for each counterclockwise step
            
            if (steps % 1) == 0:
                print(f"Steps: {round(steps)}, Variable: {my_variable}")
                totalTurns += 1
            time.sleep(delay)
            
            if steps == 20:
                turns += 1
        
        endTime = time.perf_counter()
        elapsedTime = endTime - startTime
        if elapsedTime > 1:
            print("Turns/sec =", totalTurns)
            totalTurns = 0
            startTime = time.perf_counter()
        
        lastClkState = debouncedClk
        lastDtState = debouncedDt

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

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()