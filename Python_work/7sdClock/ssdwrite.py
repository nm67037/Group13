import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(0)
GPIO.setmode(GPIO.BCM)
clk = 23
DP = 7  # DP
C = 25 # C
D = 10 # D
E = 24 # E
G = 22 # G
F = 9  # F
A = 11 # A
B = 8  # B
DFF_Pins = [clk, DP, A, B, C, D, E, F, G]
for j in range(len(DFF_Pins)): #defining gpios to dff as output
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
# while True:
#     for i in  range(len(chars)):
#         for j in range(7):
#             GPIO.output(DFF_Pins[j + 2],chars[i][j])
#             GPIO.output(clk, GPIO.HIGH)
#             sleep(.001)
#             GPIO.output(clk, GPIO.LOW)
#         sleep(1)
def printssd(input):
    for i in range(7):
        GPIO.output(DFF_Pins[i + 2],input[i])
    GPIO.output(clk, GPIO.HIGH)
    sleep(.001)
    GPIO.output(clk, GPIO.LOW)



