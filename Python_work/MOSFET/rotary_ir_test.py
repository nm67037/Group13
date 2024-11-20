import RPi.GPIO as GPIO
import time

# GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PWM_pin = 19
frequency = 1000
duty_cycle = 0.5

pwm = GPIO.PWM(PWM_pin, frequency)
pwm.start(duty_cycle)



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
desired_RPM = 0  # Variable to update with each step

startTime = time.perf_counter()
endTime = 0
elapsedTime = 0
totalTurns = 0
state = 0


def button_press():
    if state == 0:
        pwm.stop()
        print("PWM stopped")
    if state == 1:
        pwm = GPIO.PWM(PWM_pin, frequency)
        print("PWM started")

        


try:
    while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        swState = GPIO.input(sw)
        
        if swState == GPIO.LOW:
            print("Button Pressed")
            time.sleep(0.5) #replace this with an interrupt
            if state == 0:
                state = 1
                button_press()
            else:
                state = 0
                button_press()

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
                    #print("Clockwise")
                    desired_RPM += 25  # Add 25 for each clockwise step
            else:
                steps -= 0.5
                if (steps % 1) == 0:
                   # print("Counter-clockwise")
                    desired_RPM -= 25  # Subtract 25 for each counterclockwise step
            
            if (steps % 1) == 0:
                print(f"Desired RPM: {desired_RPM}") #deleted f"Steps: {round(steps)}, 
                totalTurns += 1
            time.sleep(delay)
            
            if steps == 20:
                turns += 1
        
        endTime = time.perf_counter()
        elapsedTime = endTime - startTime
        if elapsedTime > 1:
          #  print("Turns/sec =", totalTurns)
            totalTurns = 0
            startTime = time.perf_counter()
        
        lastClkState = debouncedClk
        lastDtState = debouncedDt

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()