import time 
from time import sleep
from time import perf_counter
import math

global startTime, endTime, elapsedTime
startTime = 0
endTime = 0
elapsedTime = 0
running = 1


def delayS(waitTime):
    print("Hello")
    startTime = perf_counter()
    elapsedTime = 0

    while (elapsedTime < waitTime):
        endTime = perf_counter()
        elapsedTime = endTime - startTime
        if (elapsedTime == math.floor(elapsedTime)):
            print(elapsedTime)
        ##print(elapsedTime)
        
        
    print("System delayed for ", elapsedTime, " seconds")


while running:
    print("Hello")
    delayS(5)
