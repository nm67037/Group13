import time
import RPi.GPIO as GPIO

# Define pin and constants
TELEGRAPH_PIN = 4  # Replace with the correct GPIO pin
DOT_THRESHOLD = 0.2  # Threshold for dot vs. dash in seconds
DASH_THRESHOLD = 0.6

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TELEGRAPH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_telegraph_key():
    while True:
        if GPIO.input(TELEGRAPH_PIN) == GPIO.HIGH:  # Key is pressed
            start_time = time.time()
            
            # Wait until the key is released
            while GPIO.input(TELEGRAPH_PIN) == GPIO.HIGH:
                pass
            
            # Calculate press duration
            press_duration = time.time() - start_time
            
            if press_duration < DOT_THRESHOLD:
                print("Dot")
            elif press_duration < DASH_THRESHOLD:
                print("Dash")
            else:
                print("Invalid press length")
                
        time.sleep(0.05)  # Short delay to avoid rapid polling

try:
    read_telegraph_key()
except KeyboardInterrupt:
    print("Program terminated")
finally:
    GPIO.cleanup()
