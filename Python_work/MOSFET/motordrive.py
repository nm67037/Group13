import pigpio
import RPi.GPIO as RP
from time import sleep
from math import floor
pin = 19
RP.setmode(RP.BCM)
RP.setup(pin,RP.OUT,initial=RP.HIGH)
sleep(10)
RP.cleanup()
# pi.set_PWM_frequency(pin,2000)
# #pi.set_PWM_dutycycle(pin,127)
# dutycyclepct = 0.5
# dutycycle = floor(255*dutycyclepct)

# pi.set_PWM_dutycycle(pin,dutycycle)
# # sleep(.10)
# #pi.set_PWM_dutycycle(pin,0)
# # #pi.set_PWM_frequency(pin,0)
# # sleep(.1)
# print(pi.get_mode(pin))
# # print(pi.get_PWM_frequency(pin))
# pi.write(pin,0)
# pi.stop()