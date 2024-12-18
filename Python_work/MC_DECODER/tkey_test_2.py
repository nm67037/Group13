import time
import RPi.GPIO as GPIO
import pigpio
from math import floor
pi = pigpio.pi()
# Define pin and constants
TELEGRAPH_PIN = 4  # Replace with the correct GPIO pin
DOT_THRESHOLD = 0.2  # Threshold for dot vs. dash in seconds
DASH_THRESHOLD = 0.6
global dot_length
# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TELEGRAPH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_telegraph_key():
    while True:
        if GPIO.input(TELEGRAPH_PIN) == GPIO.LOW:  # Key is pressed
            start_time = time.time()
            
            # Wait until the key is released
            while GPIO.input(TELEGRAPH_PIN) == GPIO.LOW:
                pass
            
            # Calculate press duration
            press_duration = time.time() - start_time
            print(press_duration)
            time.sleep(0.05)
            return press_duration

            # if press_duration < DOT_THRESHOLD:
            #     print("Dot")
            # elif press_duration < DASH_THRESHOLD:
            #     print("Dash")
            # else:
            #     print("Invalid press length")
                
        time.sleep(0.05)  # Short delay to avoid rapid polling
def initialize():
    global dot_length
    print("Please input Attention: - . - . -")
    d1 = read_telegraph_key()/3
    d2 = read_telegraph_key()
    d3 = read_telegraph_key()/3
    d4 = read_telegraph_key()
    d5 = read_telegraph_key()/3
    dots = [d1,d2,d3,d4,d5]
    dot_length = sum(dots)/5 #getting the average of the dot length
    print(dot_length)

def record():
    startlift = 0
    
    while 1:
        value = read_telegraph_key()
        lifttime = time.time()-startlift - value
        #print(value)

        current_word = []

        if value <= (dot_length+.2):
            print(".")
            current_word.extend(["."])


        else:
            print("-")
            current_word.extend(["-"])
        if startlift != 0: 
            if lifttime <= (dot_length+.5):
                print("ditgap")
                
            elif (dot_length + .5) < lifttime <= (dot_length+.5*3):
                print("lettergap")
                decode(current_word)
            elif (dot_length+.5*3) < lifttime <= (dot_length+.5*7):
                print("wordgap")
        startlift = time.time()


def decode(current_word):
    morse_code_dict = {

    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '-.-.-': '#', '.-.-.': '*'

    }

    string_morse_letter = ''.join(current_word)
    decoded_letter = morse_code_dict.get(string_morse_letter, "?")
    print(decoded_letter)
        

try:
    initialize()
    record()
    #read_telegraph_key()
except KeyboardInterrupt:
    print("Program terminated")
    pi.hardware_PWM(18,0,0)
finally:
    GPIO.cleanup()
