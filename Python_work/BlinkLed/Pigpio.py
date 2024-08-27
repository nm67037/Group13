import pigpio
pi=pigpio.pi()


freq = 1000
dutycycle = 100 #Duty cycle ranges from 0 (always off) to 255 (always on)

pi.set_PWM_frequency(4, freq)
pi.set_PWM_dutycycle(4, dutycycle)

#still need to add empty loop and 
#Shut the LED off with: pi.set_PWM_dutycycle(pin#, 0)
