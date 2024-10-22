import pigpio
from time import sleep

# Initialize pigpio
pi = pigpio.pi()  # Connect to pigpio daemon
if not pi.connected:
    exit()

# Setup the GPIO pin (adjust the pin number based on your circuit)
LED_PIN = 17  # Example GPIO pin connected to the speaker/microphone
pi.set_mode(LED_PIN, pigpio.OUTPUT)

# Morse code dictionary for English letters and numbers
morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
}

# Function to convert text to Morse code
def text_to_morse(text):
    morse_code = []
    for char in text.upper():
        if char in morse_code_dict:
            morse_code.append(morse_code_dict[char])
        elif char == ' ':
            morse_code.append('/')  # Use '/' to denote a space between words
        else:
            morse_code.append('?')  # Unknown characters are marked as '?'
    return morse_code

# Function to play a dot (high for x seconds)
def play_dot(dot_length):
    pi.write(LED_PIN, 1)  # Set GPIO high
    sleep(dot_length)
    pi.write(LED_PIN, 0)  # Set GPIO low
    sleep(dot_length)  # Space between dots/dashes in a letter

# Function to play a dash (high for 3x seconds)
def play_dash(dot_length):
    pi.write(LED_PIN, 1)  # Set GPIO high
    sleep(3 * dot_length)
    pi.write(LED_PIN, 0)  # Set GPIO low
    sleep(dot_length)  # Space between dots/dashes in a letter

# Function to play a Morse code sequence
def play_morse_code(morse_code_sequence, dot_length):
    for symbol in morse_code_sequence:
        if symbol == '.':
            play_dot(dot_length)
        elif symbol == '-':
            play_dash(dot_length)
        elif symbol == '/':  # Space between words
            sleep(7 * dot_length)
        sleep(3 * dot_length)  # Space between letters

# Read words from the text file (multiple lines) 
file_path = '/home/vizhins/Embedded_1/Group13/Python_work/MC_ENCODER/mcencode.txt'  # Replace with actual file path
with open(file_path, 'r') as file:
    lines = file.readlines()

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
for line in lines:
    word = line.strip()
    if word:
        morse_code_sequence = text_to_morse(word)
        print(f"Morse Code for {word}: {' '.join(morse_code_sequence)}")
        play_morse_code(morse_code_sequence, dot_length)

# Cleanup when done
pi.stop()
