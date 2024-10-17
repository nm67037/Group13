#import RPi.GPIO


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
    for char in text.upper():  # Convert to uppercase to match the dictionary
        if char in morse_code_dict:
            morse_code.append(morse_code_dict[char])
        elif char == ' ':
            morse_code.append('/')  # Use '/' to denote a space between words
        else:
            morse_code.append('?')  # Unknown characters are marked as '?'
    return ' '.join(morse_code) + ' |'  # Add '|' at the end of each Morse word

# Read words from the text file (multiple lines)
file_path = '/home/vizhins/Embedded_1/Group13/Python_work/MC_ENCODER/english.txt'  # Replace with the actual file path
with open(file_path, 'r') as file:
    lines = file.readlines()  # Read all lines from the file

# Process each word (each line) and convert to Morse code
for line in lines:
    word = line.strip()  # Strip any extra spaces or newline characters
    if word:  # Only process if the line contains a word
        morse_code = text_to_morse(word)
        print(f"{morse_code}{word}")
