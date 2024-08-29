import wiringpi
from time import sleep
wiringpi.wiringPiSetupGpio(4) #using actual GPIO number
wiringpi.softToneCreate(4) #we are using GPIO 4 for the PWM

dutycycle = .2
freq = 100
wiringpi.softToneWrite(4, freq) #this command creates the square wave
wiringpi.softPwmCreate(4,100, 100)
wiringpi.softPwmWrite(4,100)

#leftover instructions:
#Use an empty loop to keep the program running while the LED is blinking.
#Once the loop is complete, set the pin frequency to 0 to shut it off.
while True:
    print("!")
    sleep(10)
    pass

