import wiringpi as wp
import time

# Set up WiringPi
wp.wiringPiSetupGpio()

# Set the GPIO pin for PWM output (BCM pin 18)
pwm_pin = 4
wp.pinMode(pwm_pin, wp.GPIO.PWM_OUTPUT)

# Set the PWM mode to mark-space
wp.pwmSetMode(wp.GPIO.PWM_MODE_MS)

# Set the range (frequency)
wp.pwmSetRange(1024)

# Set the clock divisor (controls the frequency)
wp.pwmSetClock(32)

def set_duty_cycle(duty_cycle):
    # Convert duty cycle percentage to PWM value
    pwm_value = int(1024 * (duty_cycle / 100.0))
    wp.pwmWrite(pwm_pin, pwm_value)

try:
    while True:
        # Example: Set duty cycle to 25%
        set_duty_cycle(25)
        time.sleep(1)
        # Example: Set duty cycle to 75%
        set_duty_cycle(75)
        time.sleep(1)
except KeyboardInterrupt:
    pass

# Clean up
wp.pinMode(pwm_pin, wp.GPIO.INPUT)
