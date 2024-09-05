import pigpio
from time import sleep
pi=pigpio.pi()

pi.set_PWM_dutycycle(4,0)

freq = 10
dutycycle = .0 #Duty cycle ranges from 0 (always off) to 1 (always on)

pi.set_PWM_frequency(4, freq)
pi.set_PWM_dutycycle(4, 255 * dutycycle)
#255 is the maximum range of the dutycyle, making the dutycycle var a scaled number

dimmer = False #control this section of code by setting it true of false
if dimmer:
    pi.set_PWM_frequency(4, 2000)#set frequency above what the eye can see as flashing

while dimmer:
    for x in range(255): #change the dutycycle upward to briten the LED in a controled manner
        pi.set_PWM_dutycycle(4,x)
        sleep(.0001)
    for x in range(255): #dim the LED
        pi.set_PWM_dutycycle(4,255-x)
        sleep(.001)