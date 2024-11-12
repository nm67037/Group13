import RPi.GPIO as GPIO
from time import sleep
from time import perf_counter

global start, end, press_count, dot_length
press_count = 0
dot_length = 0
attention_length = [0] * 6

telegraph = 0   # GPIO connected to telegraph key

def start_time():
    start = perf_counter()

def read_press():
    end = perf_counter()
    duration = end - start
    if press_count < 6:
        attention_length[press_count] = duration
        press_count += 1
    elif press_count == 6:
        attention_avg = 0
        for x in attention_length:
            attention_avg += attention_length
        
        press_count += 1

    


if __name__ == '__main__':

    GPIO.add_event_detect(telegraph, GPIO.RISING, 
                          callback=start_time, bouncetime=100)
    GPIO.add_event_detect(telegraph, GPIO.FALLING,
                          callback=read_press, bouncetime=100)
    

