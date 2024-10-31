import pigpio
from time import sleep
import RPi.GPIO as GPIO
pi=pigpio.pi()
pin = 18
# pi.set_PWM_dutycycle(pin,0)
freq = 10
dutycycle = 0 #Duty cycle ranges from 0 (always off) to 1 (always on)
try:
    pi.hardware_PWM(pin,800,500000)
    while True:
        pass
except KeyboardInterrupt:
    pi.hardware_PWM(pin,0,0)
# pi.set_PWM_frequency(pin, 800)
# pi.set_PWM_dutycycle(pin, 255 * dutycycle)
# #255 is the maximum range of the dutycyle, making the dutycycle var a scaled number

# dimmer = 0 #control this section of code by setting it true of false
# if dimmer:
#     pi.set_PWM_frequency(pin, 2000)#set frequency above what the eye can see as flashing

# while dimmer:
#     for x in range(255): #change the dutycycle upward to briten the LED in a controled manner
#         pi.set_PWM_dutycycle(pin,x)
#         sleep(.0001)
#     for x in range(255): #dim the LED
#         pi.set_PWM_dutycycle(pin,255-x)
#         sleep(.001)