import tty, sys, termios
import pigpio
import os
from time import sleep
os.system('clear')
filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)
pi =pigpio.pi()
pin = 19
duty = 0
frequency = 0
x = 0
global state
state = 0
def changePWM():
    pi.hardware_PWM(pin,frequency,duty*10000)
def hardwarestate():
    global state
    if state == 0:
        state = 1
        changePWM()
    elif state == 1:
        state = 0
        pi.hardware_PWM(pin,0,0)

try:
    while 1:
        if state == 0:
            print(f"Frequency: {frequency}| Dutycycle: {duty}%| OFF")
        elif state == 1:
            print(f"Frequency: {frequency}| Dutycycle: {duty}%| ON")
        print()
        print("Controls: | F: ON/OFF|")
        print("Q: +100 hz| W: +10 hz| E: +10% DC")
        print("A: -100 hz| S: -10 hz| D: -10% DC") 
        x=sys.stdin.read(1)[0]
        if x == "q":
            frequency += 100
        elif x == "w":
            frequency += 10
        elif x == "e":
            duty += 10
        elif x == "a":
            frequency -= 100
        elif x == "s":
            frequency -= 10
        elif x == "d":
            duty -= 10
        elif x == "f":
            hardwarestate()
        if frequency > 20000:
            frequency = 20000
        elif frequency < 0:
            frequency = 0
        if duty > 100:
            duty = 100
        elif duty < 0:
            duty = 0
        os.system('clear')
        if state == 1:
            changePWM()

except KeyboardInterrupt:
    pi.hardware_PWM(pin,0,0)
    pi.stop()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)