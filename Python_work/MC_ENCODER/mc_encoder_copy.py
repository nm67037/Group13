import pigpio
from time import sleep

# Initialize pigpio
pi = pigpio.pi()  # Connect to pigpio daemon
if not pi.connected:
    exit()
pi.set_PWM_frequency(17,500)
# Setup the GPIO pin (adjust the pin number based on your circuit)
LED_PIN = 17  # Example GPIO pin connected to the speaker/microphone


# Morse code dictionary for English letters and numbers
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '#': '-.-.-', '*': '.-.-.'
}

# Function to convert text to Morse code
def t2m(text):
    morse_code = []
  
    for char in text.upper():
        if char in morse_code_dict:
            # Join dots and dashes with a single space
            morse_code.append(' '.join(morse_code_dict[char]))
        elif char == ' ':
            # Use '/' to denote a space between words
            morse_code.append('/')
        else:
            #morse_code.append('?')  # Unknown characters are marked as '?'
            pass
        # Join letters with three spaces
        return '   '.join(morse_code) + ' |'


def encode(text):
    mcode = []
    for char in text.upper():
        mcode.append(morse_code_dict[char])
    #print(mcode)
    return ' '.join(mcode)
# Function to play a dot (high for x seconds)
def play_dot(dot_length):
    #print("play dot")
    pi.set_PWM_dutycycle(17,127)  # Set GPIO high
    sleep(dot_length)
    pi.set_PWM_dutycycle(17,0)  # Set GPIO low
#    sleep(dot_length)  # Space between dots/dashes in a letter

# Function to play a dash (high for 3x seconds)
def play_dash(dot_length):
    #print("play dash")
    pi.set_PWM_dutycycle(17,127)  # Set GPIO high
    sleep(3 * dot_length)
    pi.set_PWM_dutycycle(17,0)  # Set GPIO low
#    sleep(dot_length)  # Space between dots/dashes in a letter

# Function to play a Morse code sequence
def play_morse_code(morse_code_sequence, dot_length):
    for symbol in morse_code_sequence:
        #print(symbol)
        if symbol == '.':
            play_dot(dot_length)
        elif symbol == '-':
            play_dash(dot_length)
        elif symbol == '/':  # Space between words
            #print("word end")
            sleep(7 * dot_length)
        else:
            #print("char end")
            sleep(3 * dot_length)  # Space between letters

# Read words from the text file (multiple lines) 
file_path = '/home/group13/Desktop/4230_Embedded_Group13/Group13/Python_work/MC_ENCODER/mcencode.txt'  # Replace with actual file path
with open(file_path, 'r') as file:
    lines = file.readlines()
    #print(type(lines))
    i = 1
    #print(len(lines))
    for j in range(len(lines)):
        lines.insert(i,"*")
        i += 2
    lines.insert(0,"#")
    print(lines)


# Ask user for dot length (restrict range between 0.001 and 2 seconds)
def input_dot_time():
    while True:
        try:
            dot = float(input("Dot length (in seconds, between 0.001 and 2): "))
            if 0.001 <= dot <= 2:
                return dot
            else:
                print("Please enter a value between 0.001 and 2.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


dot_length = input_dot_time()

# Process each word and convert to Morse code
if dot_length > 0.05:
    for line in lines:
        word = line.strip()
        if word:
            morse_code_sequence = t2m(word)
            print(f"Morse Code for {word}: {' '.join(morse_code_sequence)}")
            play_morse_code(morse_code_sequence, dot_length)
output_file_path = '/home/group13/Desktop/4230_Embedded_Group13/Group13/Python_work/MC_ENCODER/output.txt'
with open(output_file_path, 'w') as output:
    for line in lines:
        word = line.strip().split()  # Strip any extra spaces or newline characters
        #print(word)
        for words in word:
            #print(words)
            mcode = encode(words)
            #print(mcode)
            if (words == '#'):
                output.write(f"{mcode} | attention\n")
            elif (words == '*'):
                output.write(f"{mcode} | out\n")
            output.write(f"{mcode} | {words}\n")
            print(f"{mcode} | {words}")


# Cleanup when done
pi.stop()
