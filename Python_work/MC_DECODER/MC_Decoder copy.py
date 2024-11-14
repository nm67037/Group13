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
            
            # Calculate press duration
            #pi.hardware_PWM(spkr,0,0)
            #pi.hardware_PWM(LED_PIN,0,0)
            #GPIO.output(LED_PIN,GPIO.LOW)
            etime = time.time()
            press_duration = etime - itime
            lift_duration = itime - stime + 0.05
            #print(f"pressed for: {press_duration}, lifted for: {lift_duration}")
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
    # print(dot_length)
    # print(dot_dev)
    GPIO.add_event_detect(TELEGRAPH_PIN, GPIO.BOTH, callback=telegraphkey, bouncetime=50)
    # telegraphkey(TELEGRAPH_PIN)
#    GPIO.add_event_detect(TELEGRAPH_PIN, GPIO.RISING, callback=lift, bouncetime= 50)
def record():
    if state == 0:
        if etime < (2*dot_length - dot_dev*3):
            space = ''
            #print("1")
        elif (2*dot_length - dot_dev*3) < etime < (6*dot_length - dot_dev*3):
            space = ' '
            #print("2")
        else:
            space = '_'
            #print(f"3 {space}")
        displaylog(space)
    elif state == 1:
        if etime < (2*dot_length - dot_dev*3):
            dotdash = '.'
            # displaylog(dotdash)
            #print(".")
            pass #the input is a dot
        else:
            #print("-")
            dotdash = '-'
        displaylog(dotdash)
    # word = ''
    # current_word = '-.-.-'
    # kar = ''
    # while 1:
    #     [value,lifttime] = read_telegraph_key(0)
    #     if value <= (3*dot_length-dot_dev*5):
    #         kar = '.'
    #         #print(".")
    #     elif (3*dot_length-dot_dev*5) < value < 99:
    #         kar = '-'
    #         #print("-")
    #     else:
    #         kar = ''
            
    #     if lifttime <= (3*dot_length-dot_dev*3):
    #         current_word = current_word + kar
    #         print(f"84 {current_word}")
    #         #print("ditgap")
    #     elif (3*dot_length-dot_dev*3) < lifttime <= (7*dot_length-dot_dev*3):
    #         word= word + decode(current_word)
    #         current_word = ''
    #         current_word = current_word + kar
    #         #print("lettergap")
    #     elif (7*dot_length-dot_dev*3) < lifttime < 99:
    #         #print("wordgap")
    #         word = f'{word}{decode(current_word)} '
    #         current_word = ''
    #         current_word = current_word + kar
    #         #print(word)
    #     else:
    #         if current_word != '':
    #             word = word + f'{decode(current_word)}'
    #         current_word = ''
    #         #print(word)
    #         #break
def lift(channel):
    # global end
    # global code
    # global lettercode
    # global decodedword
    global stime
    global state
    stime = time.time() #get the start time of this loop
    state = 0

#     while GPIO.input(TELEGRAPH_PIN) == GPIO.HIGH:
#         etime = time.time() - stime
#         if etime < (2*dot_length - dot_dev*3):
            
#             #lettercode = lettercode + dotdash
#             pass #space between dots and dashes
#         elif (2*dot_length - dot_dev*3) < etime < (6*dot_length - dot_dev*3):
#             code = code + lettercode
#             decodedword = decodedword + decode(lettercode)
#             lettercode = ''
#             pass
#         else:
#             code = ''
#             #next word loop
#             pass #space between words
# #        displaylog()
    pass


def press(channel):
    global state
    global stime
    state = 1
    stime = time.time()
#     # global dotdash
#     dotdash = ''
#     time.sleep(.05)
#     global end
#     end = 0
#     stime = time.time() #get the start time of this loop
#     while GPIO.input(TELEGRAPH_PIN) == GPIO.LOW:
#         etime = time.time() - stime
#         if etime < (2*dot_length - dot_dev*3):
#             dotdash = '.'
#             pass #the input is a dot
#         else:

#             dotdash = '-'
#             #print(" - ")
#             pass #the input is a dash
#         displaylog()
#         #print("pressloopin")
#     #print("leaving pressloop")
    pass
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

    
    #     words[i] = words[i].replace(',',' ')
    # print(words[i-1])
    # print(words)
    # if state:
    #     code = input

    # else:
    #     if input == 'dotdashgap':
    #         lettercode = lettercode + code #store last dot/dash
    #         print("dotdash")
    #         #print(word + decode(lettercode))
    #     elif input == 'lettergap':
    #         lettercode = lettercode + code
    #         word = word + decode(lettercode) #store letter                
    #         wordcode = wordcode + lettercode #store code for word
    #         print("letter")
    #         #print(word)
    #         lettercode = '' #reset lettercode for next letter
    #     elif input == 'wordgap':
    #         lettercode = lettercode + code
    #         word = (word + decode(lettercode))
    #         print(word)
    #         if word == lines[line].split("|")[1].replace(' ',''):
    #             line += 1
    #         message = message + word + '\n' #store word
    #         wordcode = wordcode + lettercode
    #         messagecode = messagecode + wordcode #final storage of code
    #         lettercode = ''
    #         word = ''
    #         print("word")
    #     # code = ''
    # # os.system('clear')
    # print(lines[line])
    # print(f"{lettercode} | {word}")
    # print(message)
            #print("word")
            #print(message)

                
#◻
try:
    mc_sheet = '/home/jdieffy/Documents/Projects/ECSE4230F24/Python/Group13/Python_work/MC_DECODER/mcdecodertest.txt'
    with open(mc_sheet, 'r') as file:
        lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n","")
    
    outputfile = open("/home/jdieffy/Documents/Projects/ECSE4230F24/Python/Group13/Python_work/MC_DECODER/output.txt","w")

   #print(lines)
    initialize()

    while True: #main loop
        # record()
        pass
    #record()
    #read_telegraph_key()
except KeyboardInterrupt:
    print("Program terminated")
    pi.hardware_PWM(spkr,0,0)
    pi.hardware_PWM(LED_PIN,0,0)
    pi.stop()
    outputfile.close()
    file.close()
    GPIO.cleanup()
# finally:
#     #GPIO.cleanup()
#     print("Program terminated")
#     pi.hardware_PWM(spkr,tone,0)
#     pi.stop()
#     GPIO.cleanup()
