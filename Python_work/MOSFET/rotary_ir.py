import RPi.GPIO as GPIO
import time

# GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

clk = 22
dt = 27
sw = 7

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

try:
    while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        swState = GPIO.input(sw)
        
        if swState == GPIO.LOW:
            print("Button Pressed")
            time.sleep(0.5)
        
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

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()
