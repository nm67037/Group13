import wiringpi
from time import sleep
wiringpi.wiringPiSetupGpio() #using actual GPIO number
wiringpi.softToneCreate(4) #we are using GPIO 4 for the PWM

dutycycle = .5 #set the duty cycle of the squarewave
freq = 1 #set the frequency in hz
wiringpi.softToneWrite(4, freq) #this command creates the square wave



