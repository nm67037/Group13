with open(output_file_path, 'w') as output_file:
    # Process each word (each line) and convert to Morse code
    for line in lines:
        word = line.strip()  # Strip any extra spaces or newline characters
        if word:  # Only process if the line contains a word
            morse_code = text_to_morse(word)
            output_file.write(f"{morse_code}{word}\n")  # Write to file
            print(f"Converted: {morse_code}{word}")  # Also print to terminal