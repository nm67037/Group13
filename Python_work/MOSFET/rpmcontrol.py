import time
import RPi.GPIO as GPIO
import os
global pcnt,stime,rpm,frq,state
import pigpio
import math
import numpy as np
pi =pigpio.pi()
global duty, et, stopchanging,deeteetime,clocktime
et = np.zeros(75)
meas = np.zeros(50)
MOTOR_PIN = 19
REV_PIN = 26
CLOCK_PIN = 22
DT_PIN = 27
SW_PIN = 17
pcnt = 0
rpm = 0
duty = 100000
state = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(REV_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CLOCK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

drive_frq = 60
kp = 100
ki = 2
SRPM = 2000
SFRQ = SRPM / 20
stopchanging = False
#et = SRPM - IRPM
#Duty_cycle = Kp * et
def onff():
    global state
    if state:
        pi.hardware_PWM(MOTOR_PIN,drive_frq,0)
        state = False
    else:
        state = True
        if duty > 100000:
            changePWM()
        else:
            pi.hardware_PWM(MOTOR_PIN,drive_frq,100000)
def pulse(channel):
    global stime,pcnt,frq
    pcnt += 1
#     if pcnt == 80:
#         pcnt = 0
#         now = time.time()
#         etime = now - stime
#         stime = now
#         #os.system('clear')
#         frq = 80//etime
#         print(f"I:{frq*20} , {frq}")
#         #setduty()
def deetee(channel):
    global SFRQ,SRPM
    if GPIO.input(CLOCK_PIN):
        SFRQ -= 1.25
#         print(SFRQ*20)
    else:
        SFRQ += 1.25
#         print(SFRQ*20)
def button(channel):

    onff()
def setduty():
    global duty,et,stopchanging
    if not stopchanging:
        et = np.roll(et,1)
        error = SFRQ - frq
        et[0] = error
        #if et == np.zeros(25):
            #stopchanging = True
        prop = error * kp
        inte = np.trapz(et) * ki
        dutychange = math.floor(prop + inte)
        if -200 < dutychange < 200:
            pass
        else:
            duty += dutychange
        if duty < 50000:
            duty = 50000
        elif duty > 1000000:
            duty = 1000000
        #print(et)
        changePWM()
def changePWM():
    pi.hardware_PWM(MOTOR_PIN,drive_frq,duty)
try:
    
    GPIO.add_event_detect(REV_PIN, GPIO.FALLING, callback=pulse, bouncetime=1)
    GPIO.add_event_detect(DT_PIN, GPIO.FALLING, callback=deetee, bouncetime=50)
    GPIO.add_event_detect(SW_PIN, GPIO.FALLING, callback=button, bouncetime=800)
    stime = time.time()
    ltime = stime
    #time.sleep(1)
    pi.hardware_PWM(MOTOR_PIN,drive_frq,100000)
    lcnt = 0
    last = False
    while True:
#         if GPIO.input(REV_PIN) and not last:
#             lcnt += 1
#             last = True
#         elif not GPIO.input(REV_PIN):
#             last = False
#         if lcnt == 80:
#             now = time.time()
#             etime = now - ltime
#             ltime = now
#             lcnt = 0
#             frq = 80//etime
#             print(f"L:{frq*20} , {frq}")
#             setduty()
        meas = np.roll(meas, 1)
        time.sleep(.09)
        frq = pcnt/.09
        meas[0] = frq
        ptfrq = math.floor(np.mean(meas))
        os.system('clear')
        print(f"Set RPM: {SFRQ*20}")
        print(f"RPM:{ptfrq*20} , {ptfrq} hz")
        pcnt = 0
        if state:
            setduty()
        
        pass
except KeyboardInterrupt:
    pi.hardware_PWM(MOTOR_PIN,0,0)
    pi.stop()
    GPIO.cleanup()