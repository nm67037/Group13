import pigpio 
#import RPi.GPIO as RP
from time import sleep
from math import floor
pin = 19

pi=pigpio.pi()

pi.hardware_PWM(pin,100000,00000)


#pi.set_PWM_frequency(pin,10)
#pi.set_PWM_dutycycle(pin,)

# dutycyclepct = 0.5
# dutycycle = floor(255*dutycyclepct)

# pi.set_PWM_dutycycle(pin,dutycycle)
# # sleep(.10)
# #pi.set_PWM_dutycycle(pin,0)
# # #pi.set_PWM_frequency(pin,0)
# # sleep(.1)
#print(pi.set_mode(pin,0))
# # print(pi.get_PWM_frequency(pin))
# pi.write(pin,0)
pi.stop()