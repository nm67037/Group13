import time
import RPi.GPIO as GPIO
import pigpio
import os
import numpy as np

# Define pins
TELEGRAPH_PIN = 4
LED_PIN = 12
spkr = 18
tone = 500
# Define Global variables and initial values
global stime
global dot_length
global dot_dev
global code,message,line
global state
code = '-.-.-' #There very first character of every message is always attention
message = []
line = 1


# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TELEGRAPH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pi = pigpio.pi()

def decode(current_word):   # Take an input character array, break it up into the dots and dashes 
    word = ''               # that make up each letter in the input and put each letter back together
    code2char = {           # to make a word

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
    return word

def read_telegraph_key(option): # Called by initiallization function to gather press time and lift time
    stime = time.time()         # data for each dot and dash in attention
    while True:
        if GPIO.input(TELEGRAPH_PIN) == GPIO.LOW:   # Key is pressed
            pi.hardware_PWM(spkr,tone,500000)       # Play a sound
            pi.hardware_PWM(LED_PIN,tone,500000)    # Light the led in the least buggy way
            itime = time.time()                     # Capture the input time
            time.sleep(0.05)                        # Debounce
            while GPIO.input(TELEGRAPH_PIN) == GPIO.LOW:
                pass                                # Wait until the key is released
            pi.hardware_PWM(spkr,0,0)               # Stop the sound
            pi.hardware_PWM(LED_PIN,0,0)            # Stop the light
            
            etime = time.time()                     # Capture the end time
            press_duration = etime - itime          # difference from input time to end time is
            lift_duration = itime - stime + 0.05    # the press duration while the difference from
                                                    # start time to input time is the lift
            if option:                  # The first dash in attention will not have lift duration as it is
                return press_duration   # an unrealistic expectation of the user to start the program and wait
            else:                       # a beat before inputting the first dash
                return [press_duration,lift_duration]
            
def initialdisp(dotdash):   # When initializing it is helpful to the user to see their dots and dashes 
    os.system('clear')      # updating the interface as they start coding
    print("-.-.- | attention")
    print(f"{dotdash} | attention")

def initialize():
    global dot_length
    global dot_dev
    global stime
    os.system('clear')
    print("Please Enter:")  # Prompt the user to sign attention to start the data collection
    print("-.-.- | attention")
    d1 = read_telegraph_key(1)   	#dash
    initialdisp("-    ")
    [d2,d3] = read_telegraph_key(0) #dot
    initialdisp("-.   ")
    [d4,d5] = read_telegraph_key(0) #dash
    initialdisp("-.-  ")
    [d6,d7] = read_telegraph_key(0) #dot
    initialdisp("-.-. ")
    [d8,d9] = read_telegraph_key(0) #dash
    initialdisp("-.-.-")
    stime = time.time()     # imediately after capturing user data the start time of the input timer is recorded
    dots = [d1/3,d2,d3,d4/3,d5,d6,d7,d8/3,d9]   # data points d1, d4, and d8 are expected to be 3 unit lengths 
    dot_length = np.mean(dots)                  # as they are dashes. The rest are either dots or lifts between dots and dashs
    dot_dev = np.std(dots)  # A single unit length is considered a dot length and the users standard deviation is used 
                            # to set the tollerance of what is a dot and a dash
    GPIO.add_event_detect(TELEGRAPH_PIN, GPIO.BOTH, callback=telegraphkey, bouncetime=50)
                            # Watching the telegraph key becomes a interrupt instead of being polled
def record():   #called when the telegraph key is either pressed or released
    if state == 0:  #if the key is pressed down the elapsed time between presses is used to find what kind of space it was
        if etime < (2*dot_length - dot_dev*3): 
            space = ''  # Below 3 units and it is the space between dots and dashes in a letter
        elif (2*dot_length - dot_dev*3) < etime < (6*dot_length - dot_dev*3):
            space = ' ' # Greater than 3 but less than 7 it is the space dots and dashes in a word
        else:
            space = '_' # The space between dots and dashes between words
        displaylog(space)   # Call display log to show the new character and log it for the output file
    elif state == 1:    # if the key is released the elapsed time between releases is used to determine what character was inputted 
        if etime < (2*dot_length - dot_dev*3):
            dotdash = '.'   # Less than 3 units it is a dot
        else:

            dotdash = '-'   # Greater than 3 it is a dash
        displaylog(dotdash) # update the display and log it

def telegraphkey(channel):
    global stime
    global etime
    global state

    etime = time.time() - stime # When this interrupt occurs calculate the time since the last interrupt
    stime = time.time()         # Restart the timer
    if GPIO.input(TELEGRAPH_PIN):   # The telegraph is switch ground, so if the input is high
        state = 1                   # do not play a sound or light the led, but if the input is low
        pi.hardware_PWM(spkr,0,0)   # do play a sound and light the led
        pi.hardware_PWM(LED_PIN,0,0)# Because this interrupt is watching both rising and falling edges
    else:                           # State is used to determine what kind of edge it might have been
        state = 0
        pi.hardware_PWM(spkr,tone,500000)
        pi.hardware_PWM(LED_PIN,tone,500000)
    record()    # Call record so that the edge type and elapsed time can be used to determine the input

def displaylog(input):      # Display and log the input
    global code,message,line
    code = code + input     # Store the latest input in code
    words = code.split('_') # If the stored code has word gaps use it to separrate the dots and dashes by words
    message = [decode(i) for i in words] # Iterate through the words and decode them then store the result
    output = [f'{words[i]} | {message[i]}' for i in range(len(words))]  # Then store the coded and the word together in the
                                                                        # appropriate format
    os.system('clear')  
    print(lines[line])  # Display the word that the user is attempting to input
    print(output[-1])   # Then show them their current progress on that word

    if message[-1] == lines[line].split('| ')[1].replace(' ','') and line < len(lines):
        line += 1       # Increment to the next word the user will attempt if the word they inputted matched
    if input == '_':    # If the user inputs a word, store it in the output file
        print("printing to file")
        outputfile.write(f"{output[-2]}\n")
    elif message[-1] == 'out':      # If the user inputs the code for OUT then store that in the output and 
        outputfile.write(output[-1])# Stop writting to the file
        outputfile.close()

try:
    mc_sheet = '/home/group13/Desktop/4230_Embedded_Group13/Group13/Python_work/MC_DECODER/mcdecodertest.txt'
    with open(mc_sheet, 'r') as file:   # Open up what is essentially a music sheet for the user
        lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n","")
    # Prepare the output file to be written too
    outputfile = open("/home/group13/Desktop/4230_Embedded_Group13/Group13/Python_work/MC_DECODER/output.txt","w")
    
    initialize()

    while True: #main loop
        pass

except KeyboardInterrupt:       # IF the program is terminated, stop playing sound lighting leds and end control
    print("Program terminated") # of the GPIOS, also close the open files.
    pi.hardware_PWM(spkr,0,0)
    pi.hardware_PWM(LED_PIN,0,0)
    pi.stop()
    outputfile.close()
    file.close()
    GPIO.cleanup()