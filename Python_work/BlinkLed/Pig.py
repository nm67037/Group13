import pigpio
pi=pigpio.pi()

print(pi.get_PWM_range)

pi.set_PWM_dutycycle(4,0)

freq = 2000
dutycycle = 0 #Duty cycle ranges from 0 (always off) to 255 (always on)

pi.set_PWM_frequency(4, freq)
pi.set_PWM_dutycycle(4, 255 * dutycycle)

#still need to add empty loop and 
#Shut the LED off with: pi.set_PWM_dutycycle(pin#, 0)
