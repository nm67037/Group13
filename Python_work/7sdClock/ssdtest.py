import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(0)
GPIO.setmode(GPIO.BCM)
clk = 23
D1 = 7 #seg
D2 = 25
D3 = 10
D4 = 24
D5 = 22
D6 = 9
D7 = 11
D8 = 8
GPIO.setup(clk,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(D1,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(D2,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(D3,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(D4,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(D5,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(D6,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(D7,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(D8,GPIO.OUT,initial=GPIO.HIGH)


# GPIO.output(D1, GPIO.HIGH)
# GPIO.output(D2, GPIO.HIGH)
# GPIO.output(D3, GPIO.HIGH)
# GPIO.output(D4, GPIO.HIGH)
# GPIO.output(D5, GPIO.HIGH)
# GPIO.output(D6, GPIO.HIGH)
# GPIO.output(D7, GPIO.HIGH)
# GPIO.output(D8, GPIO.HIGH)

GPIO.output(clk, GPIO.HIGH)
sleep(1)
GPIO.output(clk, GPIO.LOW)



