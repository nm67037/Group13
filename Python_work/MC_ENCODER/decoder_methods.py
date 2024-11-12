import RPi.GPIO as GPIO
from time import sleep
from time import perf_counter

global start, end, press_count, dot_length
press_count = 0
dot_length = 0
attention_length = [0] * 5

telegraph = 0   # GPIO connected to telegraph key

def start_time():
    start = perf_counter()

def read_press():
    end = perf_counter()
    duration = end - start
    if press_count < 5:
        attention_length[press_count] = duration
        press_count += 1
    elif press_count == 5:
        ## Sums up the total length of the dots
        dot_total = attention_length[1] + attention_length[3]
        ## Sums up the total length of the dashes
        dash_total = attention_length[0] + attention_length[2] + attention_length[4]
        ## Finds the average dot length based upon the prior two sums
        dot_length = ((dot_total / 2) + (dash_total / 9)) / 2
        
        press_count += 1
    else: 
        ## MAKE SURE TO ACCOUNT FOR TOLERANCES ON DOT_LENGTH BEFORE RUNNING, OTHERWISE THE PROGRAM WILL NEVER READ INPUT 
        if duration == dot_length: # Include tolerances here
            play_dot(dot_length) # This function is implemented in the mc_encoder files
        elif duration == (3 * dot_length): # Include tolerances here
            play_dash(dot_length)
        


if __name__ == '__main__':

    GPIO.add_event_detect(telegraph, GPIO.RISING, 
                          callback=start_time, bouncetime=100)
    GPIO.add_event_detect(telegraph, GPIO.FALLING,
                          callback=read_press, bouncetime=100)
    

