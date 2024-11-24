import time     # Import the necessary Libraries for the project
import RPi.GPIO as GPIO
import os
import pigpio
import math
import numpy as np

pi = pigpio.pi()    # connect to the pigpio daemon

global duty, et, pcnt, state, SFRQ  # List global variables

MOTOR_PIN = 19  #list of used GPIOS and their names
REV_PIN = 26
CLOCK_PIN = 22
DT_PIN = 27
SW_PIN = 17

et = np.zeros(75)   #initialize variables and arrays
meas = np.zeros(50)
pcnt = 0    #The pulse count from the IR sensor
duty = 100000   #The inital duty cycle until the PI control takes control
state = True
drive_frq = 60  #The frequency by which the motor reveives its PWM signal
kp = 100    #The proportion gain
ki = 2      #The integral gain
SRPM = 2000 #The inital target RPM
SFRQ = SRPM / 20    #The target frequency based on the target RPM

GPIO.setmode(GPIO.BCM)  # Setup GPIOS for taking an input singal
GPIO.setup(REV_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #output from the IR sensor
GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CLOCK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def onff(channel):  #Controls the state of the motor if the rotory encoder is pressed
    global state
    if state:   #If the motor is spinning stop it from spinning and set the flag
        pi.hardware_PWM(MOTOR_PIN,drive_frq,0)
        state = False
    else:       #If the motor is not spinning make sure the current duty cycle is high enough   
        state = True #If it is high enough give it the dutycycle it had before it was stopped and rest the flag
        if duty > 100000:
            changePWM()
        else:
            pi.hardware_PWM(MOTOR_PIN,drive_frq,100000)

def pulse(channel): #If the IR has a pulse from a blade up the count by one
    global pcnt
    pcnt += 1

def deetee(channel):    #If the DT pin has a rising edge check the state of the clock pin
    global SFRQ         #and change the target frequency accordingly
    if GPIO.input(CLOCK_PIN):
        SFRQ -= 1.25
    else:
        SFRQ += 1.25

def setduty():
    global duty,et
    et = np.roll(et,1)  #To get an integral keep track of the error over time
    error = SFRQ - frq  #by rolling one the right the array keeps the last 75 error amounts
    et[0] = error
    prop = error * kp   #The proportonal adjustment is the current error times the gain
    inte = np.trapz(et) * ki    #The integral adjustment is the integral of the 75 error amouts times the gain
    dutychange = math.floor(prop + inte) #The amount that the dutycycle will change by is the sum of the P and I
    if -200 > dutychange > 200: #If the change is outside the deadzone add it to the current dutycycle
        duty += dutychange

    if duty < 50000: #if the duty cycle tries to go outside of these bounds it is stopped
        duty = 50000
    elif duty > 1000000:
        duty = 1000000
    changePWM() #Calling the change in duty cycle

def changePWM():
    pi.hardware_PWM(MOTOR_PIN,drive_frq,duty)

try:
    GPIO.add_event_detect(REV_PIN, GPIO.FALLING, callback=pulse, bouncetime=1)  #setup the interupts from the ir and rotary encoder
    GPIO.add_event_detect(DT_PIN, GPIO.FALLING, callback=deetee, bouncetime=50)
    GPIO.add_event_detect(SW_PIN, GPIO.FALLING, callback=onff, bouncetime=800)

    pi.hardware_PWM(MOTOR_PIN,drive_frq,100000) #Start the motor so we can start adjusting the duty cycle to get the target RPM

    while True:
        meas = np.roll(meas, 1) #Get a rolling average of the measured frquency to make it easier to read in the consol
        time.sleep(.09) #The amount of time we will count IR pulses before making changes
        frq = pcnt/.09  #calculate the frequency by from the amount of time we counted IR pulses for and the number of IR pulses we counted
        meas[0] = frq   #add the the new frequency to the rolling average array
        ptfrq = math.floor(np.mean(meas))   #The frequency we will print to the consol

        os.system('clear')
        print(f"Set RPM: {SFRQ*20}")    #it is less math to work by frequency instead of RPM so RPM is only calculated when we print it
        print(f"RPM:{ptfrq*20} , {ptfrq} hz")

        pcnt = 0    #Reset the count every loop

        if state:   #If the motor should be on than the duty cycle can be updated
            setduty()

except KeyboardInterrupt:   #If the program is stopped, stop the motor and clean up the GPIO
    pi.hardware_PWM(MOTOR_PIN,0,0)
    pi.stop()
    GPIO.cleanup()