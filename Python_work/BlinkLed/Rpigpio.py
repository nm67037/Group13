import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(0)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT,initial=GPIO.LOW)

freq = 1 #Frequency in herts
per = 1/freq #period of the square wave
dutycycle = .5 #number 0-1 .4 for 40% duty cycle high
h = per * dutycycle # Calculate the time spent high 
l = per - h			# then set the remainder of the period for low

while True:
    GPIO.output(4, GPIO.HIGH) #command high
    sleep(h)
    GPIO.output(4,GPIO.LOW) #command low
    sleep(l)
    
