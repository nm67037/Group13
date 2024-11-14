import time
import RPi.GPIO as GPIO
import pigpio
import os
import numpy as np
pi = pigpio.pi()
# Define pin and constants
TELEGRAPH_PIN = 4  # Replace with the correct GPIO pin
global stime
global dot_length
global dot_dev
global initialized
global odd #old dot dash
global code,lettercode,wordcode,messagecode,word,message,line
global state
initialized = 0
dot_length = 99
LED_PIN = 12
spkr = 18
tone = 800
dotdash = ''
odd = 'startup'
code = '-.-.-'
lettercode = ''
wordcode = ''
messagecode = ''
word = ''
message = []
line = 1
# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TELEGRAPH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def decode(current_word):
    word = ''
    code2char = {

    '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f',
    '--.': 'g', '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l',
    '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r',
    '...': 's', '-': 't', '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
    '-.--': 'y', '--..': 'z', '-----': '0', '.----': '1', '..---': '2',
    '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '-.-.-': 'attention', '.-.-.': 'out', '':'◻'

    }
    letters = current_word.split(' ')
    for i in range(len(letters)):
        word = word + code2char.get(letters[i], "?")
    #print(decoded_letter)
    return word
def read_telegraph_key(option):
    stime = time.time()
    while True:
        if GPIO.input(TELEGRAPH_PIN) == GPIO.LOW:  # Key is pressed
            #print(GPIO.input(TELEGRAPH_PIN))
            #pi.hardware_PWM(spkr,tone,500000)
            #pi.hardware_PWM(LED_PIN,tone,500000)
            itime = time.time()
            time.sleep(0.05)#debounce
            # Wait until the key is released
            while GPIO.input(TELEGRAPH_PIN) == GPIO.LOW:
                pass
            etime = time.time()
            press_duration = etime - itime
            lift_duration = itime - stime + 0.05

            if option:
                return press_duration
            else:
                return [press_duration,lift_duration]
        timeout = time.time() - stime
        if timeout > (10 or dot_length*10) and initialized == 1:
             #print("timeout")
             return [99,99]
    
        #time.sleep(0.05)  # Short delay to avoid rapid polling
def initialdisp(dotdash):
    os.system('clear')
    print("-.-.- | attention")
    print(f"{dotdash} | attention")
def initialize():
    global dot_length
    global dot_dev
    global initialized
    global stime
    os.system('clear')
    print("Please Enter:")
    print("-.-.- | attention")
    d1 = read_telegraph_key(1)/3 	#dash
    initialdisp("-    ")
    [d2,d3] = read_telegraph_key(0) #dot
    initialdisp("-.   ")
    [d4,d5] = read_telegraph_key(0) #dash
    initialdisp("-.-  ")
    [d6,d7] = read_telegraph_key(0) #dot
    initialdisp("-.-. ")
    [d8,d9] = read_telegraph_key(0) #dash
    initialdisp("-.-.-")
    stime = time.time()
    dots = [d1,d2,d3,d4/3,d5,d6,d7,d8/3,d9]
    dot_length = np.mean(dots)
    dot_dev = np.std(dots)

    GPIO.add_event_detect(TELEGRAPH_PIN, GPIO.BOTH, callback=telegraphkey, bouncetime=50)

def record():
    if state == 0:
        if etime < (2*dot_length - dot_dev*3):
            space = ''
        elif (2*dot_length - dot_dev*3) < etime < (6*dot_length - dot_dev*3):
            space = ' '
        else:
            space = '_'
        displaylog(space)
    elif state == 1:
        if etime < (2*dot_length - dot_dev*3):
            dotdash = '.'
        else:

            dotdash = '-'
        displaylog(dotdash)

def telegraphkey(channel):
    global stime
    global etime
    global state

    etime = time.time() - stime
    stime = time.time() #get the start time of this loop
    if GPIO.input(TELEGRAPH_PIN):
        state = 1
        #pi.hardware_PWM(spkr,0,0)
        #pi.hardware_PWM(LED_PIN,0,0)
    else:
        state = 0
        #pi.hardware_PWM(spkr,tone,500000)
        #pi.hardware_PWM(LED_PIN,tone,500000)
    record()
def displaylog(input):#display and log the input
    global code,message,line
    code = code + input
    words = code.split('_')
    message = [decode(i) for i in words]
    output = [f'{words[i]} | {message[i]}' for i in range(len(words))]

    os.system('clear')
    print(lines[line])
    print(output[-1])

    if message[-1] == lines[line].split('| ')[1].replace(' ','') and line < len(lines):
        line += 1
    if input == '_':
        print("printing to file")
        outputfile.write(f"{output[-2]}\n")
    elif message[-1] == 'out':
        outputfile.write(output[-1])
        outputfile.close()

try:
    mc_sheet = '/home/jdieffy/Documents/Projects/ECSE4230F24/Python/Group13/Python_work/MC_DECODER/mcdecodertest.txt'
    with open(mc_sheet, 'r') as file:
        lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n","")
    
    outputfile = open("/home/jdieffy/Documents/Projects/ECSE4230F24/Python/Group13/Python_work/MC_DECODER/output.txt","w")


    initialize()

    while True: #main loop

        pass

except KeyboardInterrupt:
    print("Program terminated")
    pi.hardware_PWM(spkr,0,0)
    pi.hardware_PWM(LED_PIN,0,0)
    pi.stop()
    outputfile.close()
    file.close()
    GPIO.cleanup()

