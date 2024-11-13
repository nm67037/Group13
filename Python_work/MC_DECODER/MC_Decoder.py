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
LED_PIN = 12
spkr = 18
tone = 800
# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TELEGRAPH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# def encode(input):
#     char2code = {
#     'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
#     'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
#     'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
#     's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
#     'y': '-.--', 'z': '--..',
#     '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
#     '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
#     '#': '-.-.-', '*': '.-.-.'
#     }
#     encoded_letter = char2code.get(input,'?')
#     print(encoded_letter)
#     return encoded_letter
def decode(current_word):
    code2char = {

    '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f',
    '--.': 'g', '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l',
    '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r',
    '...': 's', '-': 't', '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
    '-.--': 'y', '--..': 'z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '-.-.-': 'attention', '.-.-.': 'out'

    }

    decoded_letter = code2char.get(current_word, "?")
    print(decoded_letter)
    return decoded_letter
def read_telegraph_key(option):
    stime = time.time()
    while True:
        if GPIO.input(TELEGRAPH_PIN) == GPIO.LOW:  # Key is pressed
            pi.hardware_PWM(spkr,tone,500000)
            pi.hardware_PWM(LED_PIN,tone,500000)
            itime = time.time()
            
            # Wait until the key is released
            while GPIO.input(TELEGRAPH_PIN) == GPIO.LOW:
                pass
            
            # Calculate press duration
            pi.hardware_PWM(spkr,0,0)
            pi.hardware_PWM(LED_PIN,0,0)
            #GPIO.output(LED_PIN,GPIO.LOW)
            etime = time.time()
            press_duration = etime - itime
            lift_duration = itime - stime + 0.05
            #print(f"pressed for: {press_duration}, lifted for: {lift_duration}")
            time.sleep(0.05)
            if option:
                return press_duration
            else:
                return [press_duration,lift_duration]
        timeout = time.time() - stime
        if timeout > (10 or dot_length*10) and initialized == 1:
             #print("timeout")
             return [99,99]
    
        time.sleep(0.05)  # Short delay to avoid rapid polling
def initialize():
    global dot_length
    global dot_dev
    global initialized
    print("Please Enter:")
    print("-.-.- | attention")
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
    GPIO.add_event_detect(TELEGRAPH_PIN, GPIO.FALLING, callback=pressloop, bouncetime=50)
def record():
    word = ''
    current_word = '-.-.-'
    kar = ''
    while 1:
        [value,lifttime] = read_telegraph_key(0)
        if value <= (3*dot_length-dot_dev*5):
            kar = '.'
            #print(".")
        elif (3*dot_length-dot_dev*5) < value < 99:
            kar = '-'
            #print("-")
        else:
            kar = ''
            
        if lifttime <= (3*dot_length-dot_dev*3):
            current_word = current_word + kar
            print(f"84 {current_word}")
            #print("ditgap")
        elif (3*dot_length-dot_dev*3) < lifttime <= (7*dot_length-dot_dev*3):
            word= word + decode(current_word)
            current_word = ''
            current_word = current_word + kar
            #print("lettergap")
        elif (7*dot_length-dot_dev*3) < lifttime < 99:
            #print("wordgap")
            word = f'{word}{decode(current_word)} '
            current_word = ''
            current_word = current_word + kar
            #print(word)
        else:
            if current_word != '':
                word = word + f'{decode(current_word)}'
            current_word = ''
            #print(word)
            #break
def liftloop():
    global end
    stime = time.time() #get the start time of this loop
    end = 0
    while GPIO.input(TELEGRAPH_PIN) == GPIO.HIGH:
        etime = time.time() - stime
        if etime < (3*dot_length - dot_dev*3):
            print("dotdash gap")
            pass #space between dots and dashes
        elif (3*dot_length - dot_dev*3) < etime < (7*dot_length - dot_dev*3):
            print("lettergap")
            pass #space between letters
        else:
            print("wordgap")
            end = 1 #sit in end loop after word logic and do nothing until key inturrupt
            pass #space between words
        while end:
            #print("end loopin")
            pass

def pressloop(channel):
    time.sleep(.05)
    global end
    end = 0
    stime = time.time() #get the start time of this loop
    while GPIO.input(TELEGRAPH_PIN) == GPIO.LOW:
        etime = time.time() - stime
        if etime < (3*dot_length - dot_dev*3):
            print(" . ")
            pass #the input is a dot
        else:
            print(" - ")
            pass #the input is a dash
        print("pressloopin")
    print("leaving pressloop")
try:
    initialize()
    while True: #main loop
        #print("mainloopin")
        liftloop()
    #record()
    #read_telegraph_key()
except KeyboardInterrupt:
    print("Program terminated")
    pi.hardware_PWM(spkr,0,0)
    pi.hardware_PWM(LED_PIN,0,0)
    pi.stop()
    GPIO.cleanup()
# finally:
#     #GPIO.cleanup()
#     print("Program terminated")
#     pi.hardware_PWM(spkr,tone,0)
#     pi.stop()
#     GPIO.cleanup()
