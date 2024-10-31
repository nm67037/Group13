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
            # Join dots and dashes with a single space
            morse_code.append(' '.join(morse_code_dict[char]))
        elif char == ' ':
            # Use '/' to denote a space between words
            morse_code.append('/')
        else:
            morse_code.append('?')  # Unknown characters are marked as '?'
    # Join letters with three spaces
    return '   '.join(morse_code) + ' |'

# Read words from the text file (multiple lines)
file_path = '/home/vizhins/Embedded_1/Group13/Python_work/MC_ENCODER/mcencode.txt'  # Replace with the actual file path
with open(file_path, 'r') as file:
    lines = file.readlines()

# Process each word (each line) and convert to Morse code
for line in lines:
    word = line.strip()  # Strip any extra spaces or newline characters
    if word:  # Only process if the line contains a word
        morse_code = text_to_morse(word)
        print(f"{morse_code}{word}")

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

