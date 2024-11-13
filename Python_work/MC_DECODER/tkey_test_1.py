import time
import RPi.GPIO as GPIO
import pigpio
from math import floor
import numpy as np
pi = pigpio.pi()
# Define pin and constants
TELEGRAPH_PIN = 4  # Replace with the correct GPIO pin
global dot_length
global dot_dev
global initialized
initialized = 0
dot_length = 99
spkr = 18
tone = 800
# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TELEGRAPH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def decode(current_word):
    morse_code_dict = {

    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '-.-.-': 'ATTENTION', '.-.-.': 'OUT'

    }

    string_morse_letter = ''.join(current_word)
    decoded_letter = morse_code_dict.get(string_morse_letter, "?")
    print(decoded_letter)
    return decoded_letter
def read_telegraph_key(option):
    stime = time.time()
    while True:
        if GPIO.input(TELEGRAPH_PIN) == GPIO.LOW:  # Key is pressed
            pi.hardware_PWM(spkr,tone,50000)
            pi.write(12,1)
            itime = time.time()
            
            # Wait until the key is released
            while GPIO.input(TELEGRAPH_PIN) == GPIO.LOW:
                pass
            
            # Calculate press duration
            pi.hardware_PWM(spkr,0,0)
            pi.write(12,0)
            etime = time.time()
            press_duration = etime - itime
            lift_duration = itime - stime + 0.05
            print(f"pressed for: {press_duration}, lifted for: {lift_duration}")
            time.sleep(0.05)
            if option:
                return press_duration
            else:
                return [press_duration,lift_duration]
        timeout = time.time() - stime
        if timeout > (10 or dot_length*10) and initialized == 1:
             print("timeout")
             return [99,99]
    
        time.sleep(0.05)  # Short delay to avoid rapid polling
def initialize():
    global dot_length
    global dot_dev
    global initialized
    print("Please input Attention: - . - . -")
    d1 = read_telegraph_key(1)/3 	#dash
    [d2,d3] = read_telegraph_key(0) #dot
    [d4,d5] = read_telegraph_key(0) #dash
    [d6,d7] = read_telegraph_key(0) #dot
    [d8,d9] = read_telegraph_key(0) #dash
    dots = [d1,d2,d3,d4/3,d5,d6,d7,d8/3,d9]
    dot_length = np.mean(dots)
    dot_dev = np.std(dots)
    initialized = 1
    print(dot_length)
    print(dot_dev)

def record():
    word = ''
    current_word = '-.-.-'
    kar = ''
    while 1:
        [value,lifttime] = read_telegraph_key(0)
        if value <= (3*dot_length-dot_dev*5):
            kar = '.'
            print(".")
        elif (3*dot_length-dot_dev*5) < value < 99:
            kar = '-'
            print("-")
        else:
            kar = ''
            
        if lifttime <= (3*dot_length-dot_dev*5):
            current_word = current_word + kar
            print(f"84 {current_word}")
            print("ditgap")
        elif (3*dot_length-dot_dev*5) < lifttime <= (7*dot_length-dot_dev*5):
            word= word + decode(current_word)
            current_word = ''
            current_word = current_word + kar
            print("lettergap")
        elif (7*dot_length-dot_dev*5) < lifttime < 99:
            print("wordgap")
            word = f'{word}{decode(current_word)} '
            current_word = ''
            current_word = current_word + kar
            print(word)
        else:
            if current_word != '':
                word = word + f'{decode(current_word)}'
            current_word = ''
            print(word)
            #break
            

try:
    initialize()
    record()
    #read_telegraph_key()
except KeyboardInterrupt:
    print("Program terminated")
    pi.hardware_PWM(18,0,0)
finally:
    GPIO.cleanup()
    print("Program terminated")
    pi.hardware_PWM(18,0,0)
