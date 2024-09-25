import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(0)
GPIO.setmode(GPIO.BCM)
led = 6
clk0 = 5
clk1 = 7
clk2 = 16
clk3 = 12
DP = 11  # D-flip-flop input: 4D, 4Q
A = 25 # input: D6, output: Q6
B = 8 # input: 5D, output: 5Q
C = 9 # input: 3D, output: 3Q
D = 23 # input: 2D, output: 2Q
E = 22 # input: 1D, output: 1Q
F = 10 # input: 7D, output: 7Q
G = 24 # input: 8D, output: 8Q

DFF_Pins = [led, clk0, clk1, clk2, clk3, DP, A, B, C, D, E, F, G]
for j in range(len(DFF_Pins)): #defining gpios to dff as output
    print(DFF_Pins[j])
    GPIO.setup(DFF_Pins[j], GPIO.OUT,initial=GPIO.LOW)
#chars = [cA, cB, cC, cD, N1, N2, N3, N4, N5, N6, N7, N8, N9]

cA = [1, 1, 1, 0, 1, 1, 1]
cB = [0, 0, 1, 1, 1, 1, 1]
cC = [1, 0, 0, 1, 1, 1, 0]
cD = [0, 1, 1, 1, 1, 0, 1]
N1 = [0, 1, 1, 0, 0, 0, 0]
N2 = [1, 1, 0, 1, 1, 0, 1]
N3 = [1, 1, 1, 1, 0, 0, 1]
N4 = [0, 1, 1, 0, 0, 1, 1]
N5 = [1, 0, 1, 1, 0, 1, 1]
N6 = [1, 0, 1, 1, 1, 1, 1]
N7 = [1, 1, 1, 0, 0, 0, 0]
N8 = [1, 1, 1, 1, 1, 1, 1]
N9 = [1, 1, 1, 0, 0, 1, 1]
N0 = [1, 1, 1, 1, 1, 1, 0]
chars = [cA, cB, cC, cD, N1, N2, N3, N4, N5, N6, N7, N8, N9, N0]

def printssd(input,clock):
    for i in range(7):
        GPIO.output(DFF_Pins[i + 6],input[i])
    GPIO.output(clock, GPIO.HIGH)
    sleep(.001)
    GPIO.output(clock, GPIO.LOW)

while True:
    for i in  range(len(chars)):
        print(chars[i])
        printssd(chars[i],clk0)
        printssd(chars[i],clk1)
        printssd(chars[i],clk2)
        printssd(chars[i],clk3)
        sleep(1)