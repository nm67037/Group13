import RPi.GPIO as GPIO
import time
import os
global pcnt,stime,rpm
import pigpio
import math
import numpy as np
pi =pigpio.pi()
global duty, et, stopchanging
et = np.zeros(50)
MOTOR_PIN = 19
REV_PIN = 26
pcnt = 0
rpm = 0
duty = 100000
GPIO.setmode(GPIO.BCM)
GPIO.setup(REV_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
drive_frq = 180
kp = 60
ki = .1
SRPM = 0
stopchanging = False

# GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def pulse(channel):
    global stime,pcnt,rpm
    pcnt += 1
    if pcnt == 24:
        pcnt = 0
        now = time.time()
        etime = now - stime
        stime = now
        os.system('clear')
        rpm = 8/etime * 60
        print(rpm)
        setduty()

def setduty():
    global duty,et,stopchanging
    if not stopchanging:
        et = np.roll(et,1)
        error = SRPM - rpm
        et[0] = error
        #if et == np.zeros(25):
            #stopchanging = True
        prop = et[0] * kp
        inte = np.trapz(et) * ki
        dutychange = math.floor(prop + inte)
        if -20000 < dutychange < 20000:
            pass
        else:
            duty += dutychange
        if duty < 50000:
            duty = 50000
        elif duty > 1000000:
            duty = 1000000
       # print(et)
        changePWM()

def changePWM():
    pi.hardware_PWM(MOTOR_PIN,drive_frq,duty)


PWM_pin = 19
frequency = 1000
duty_cycle = 0.5

GPIO.setup(PWM_pin, GPIO.OUT)
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
    GPIO.add_event_detect(REV_PIN, GPIO.FALLING, callback=pulse, bouncetime=1)
    stime = time.time()
    time.sleep(1)
    pi.hardware_PWM(MOTOR_PIN,drive_frq,100000)
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
                    SRPM = desired_RPM
            else:
                steps -= 0.5
                if (steps % 1) == 0:
                   # print("Counter-clockwise")
                    desired_RPM -= 25  # Subtract 25 for each counterclockwise step
                    SRPM = desired_RPM
            
            if (steps % 1) == 0:
                print(f"Desired RPM: {desired_RPM}") #deleted f"Steps: {round(steps)}, 
                print(f"Measured RPM: {rpm}")
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
    pi.hardware_PWM(MOTOR_PIN,0,0)
    pi.stop()
    GPIO.cleanup()
finally:
    GPIO.cleanup()