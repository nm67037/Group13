import time
import RPi.GPIO as GPIO
import os
global pcnt,stime,rpm
import pigpio
import math
import numpy as np
pi =pigpio.pi()
global duty, et
et = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
MOTOR_PIN = 19
REV_PIN = 26
pcnt = 0
rpm = 0
duty = 100000
GPIO.setmode(GPIO.BCM)
GPIO.setup(REV_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
drive_frq = 160
kp = 40
ki = .2
SRPM = 250

#et = SRPM - IRPM
#Duty_cycle = Kp * et
def pulse(channel):
    global stime,pcnt,rpm
    pcnt += 1
    if pcnt == 30:
        pcnt = 0
        now = time.time()
        etime = now - stime
        stime = now
        os.system('clear')
        rpm = 10/etime * 60
        print(rpm)
        setduty()
def setduty():
    global duty,et
    et = np.roll(et,1)
    et[0] = SRPM - rpm
    prop = et[0] * kp
    inte = np.trapz(et) * ki
    duty += math.floor(prop + inte)
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