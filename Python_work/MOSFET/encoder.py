import pigpio
from pigpio_encoder import Rotary 
import time
import sys

#initializing pi
pi = pigpio.pi()

#setting up counter for rotations
global seconds
seconds = 0

global cw_turns
cw_turns = 0

global cc_turns
cc_turns = 0

#prints when neither callback function is being used
print("None")

#clockwise function 
def clockwise():
    global cw_turns
    cw_turns += 1
    print("Clockwise")

#counter-clockwise function
def cclockwise():
    global cc_turns
    cc_turns += 1
    print("Counter clockwise")

#button press function
def press():
    print("Press")

#initializing encoder clk, dt, and sw pins
encoder = Rotary(clk_gpio=xx, dt_gpio=xx, sw_gpio=xx)

#setting up callback functions
encoder.setup_rotary(up_callback=clockwise,
    down_callback=cclockwise
)

#initializing callback function when encoder is pressed
encoder.setup_switch(sw_short_callback=press)

#infinite while loop to track encoder state
while True:
		my_rotary.watch()
		time.sleep()
