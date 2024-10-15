import pigpio
from pigpio_encoder import Rotary 
import time
import sys

#initializing pi
pi = pigpio.pi()

#setting up counter for rotations
global seconds, cw_step, cc_step, turns
seconds = 0
cw_step = 0
cc_step = 0
turns = 0

#clockwise function 
def clockwise():
    global turns, cw_step, cc_step
    
    cw_step += 1
    print("Clockwise")
    
    if (cw_step == 20):
        turns += 1
        cw_step = 0

    if (cc_step > 1):
        cc_step -= 1
   
    #print("steps: ", cw_step)
    #print("turns: ", turns)

#counter-clockwise function
def cclockwise():
    global turns, cc_step, cw_step
    cc_step += 1

    if (cc_step == 20): #20 steps in 1 full rotation
         turns += 1
         cc_step = 0

    if (cw_step > 1):
        cw_step -= 1


    print("Counter clockwise")
    #print("steps: ", cc_step)
    #print("turns: ", turns)

#button press function
def press():
    print("Press")

#initializing encoder clk, dt, and sw pins
encoder = Rotary(clk_gpio=6, dt_gpio=5, sw_gpio=16)

#setting up callback functions
encoder.setup_rotary(up_callback=cclockwise,
    down_callback=clockwise
)

#initializing callback function when encoder is pressed
encoder.setup_switch(sw_short_callback=press)

#infinite while loop to track encoder state
while True:
	time.sleep(1)
	seconds += 1
	tps = float(turns)/seconds
	#prints when encoder not in use
	print("None")
	print("turns/second: ", tps)
