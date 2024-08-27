import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(0)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT,initial=GPIO.LOW)

freq = 1000
per = 1/freq
x = per/2

while True:
    GPIO.output(4, GPIO.HIGH)
    sleep(x)
    GPIO.output(4,GPIO.LOW)
    sleep(x)
