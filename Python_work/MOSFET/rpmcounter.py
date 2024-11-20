import time
import RPi.GPIO as GPIO
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
SRPM = 2500
stopchanging = False
#et = SRPM - IRPM
#Duty_cycle = Kp * et
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
        print(et)
        changePWM()
def changePWM():
    pi.hardware_PWM(MOTOR_PIN,drive_frq,duty)
try:
    
    GPIO.add_event_detect(REV_PIN, GPIO.FALLING, callback=pulse, bouncetime=1)
    stime = time.time()
    time.sleep(1)
    pi.hardware_PWM(MOTOR_PIN,drive_frq,100000)
    while True:
        pass
except KeyboardInterrupt:
    pi.hardware_PWM(MOTOR_PIN,0,0)
    pi.stop()
    GPIO.cleanup()