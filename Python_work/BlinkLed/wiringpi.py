import wiringpi
wiringpi.wiringPiSetupGpio() #using actual GPIO number
wiringpi.softToneCreate(4) #we are using GPIO 4 for the PWM


freq = 1000
wiringpi.softToneWrite(4, freq) #this command creates the square wave

#leftover instructions:
#Use an empty loop to keep the program running while the LED is blinking.
#Once the loop is complete, set the pin frequency to 0 to shut it off.

