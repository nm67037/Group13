import RPi.GPIO as GPIO
import time
from time import sleep
#GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
pin = 19

GPIO.setup(pin,GPIO.OUT)
freq = 50
pwm=GPIO.PWM(pin,freq)

pwm.start(0)

#pwm.ChangeDutyCycle(20)
#time.sleep(2)
#pwm.ChangeDutyCycle(50)
#time.sleep(2)
pwm.ChangeDutyCycle(100)
time.sleep(7)

pwm.stop()
GPIO.cleanup()


#try:
 #   while True:
  #      for duty_cycle in range(0,100,1):
   #         pwm.ChangeDutyCycle(duty_cycle)
    #        time.sleep(0.05)
     #   for duty_cycle in range (100,0,-1):
      #      pwm.ChangeDutyCycle(duty_cycle)
       #     time.sleep(0.05)
        
#except KeyboardInterrupt:
 #   pass

#pwm.stop()
#GPIO.cleanup()