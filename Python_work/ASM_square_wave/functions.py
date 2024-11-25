import time
import subprocess
import os
from time import sleep

class square_wave:
    def __init__(self,frequency):
        self.frequency=frequency
        with open('/home/vizhins/Embedded_1/Group13/Python_work/ASM_square_wave/assembly.s') as file:
            lines=[line.rstrip() for line in file.readlines()] #open and read the .s file
            for line in lines:
                if 'delay' in line:
                    lines[lines.index(line)]='delay:  .asciz'+delay+'\\n' #this is supposed to replace the current delay value in the .s to the new one, derived from the desired frequency
       #below we will rewrite the whole .s file with the new delay: 
        with open('/home/vizhins/Embedded_1/Group13/Python_work/ASM_square_wave/assembly.s','w') as file:
            for line in lines:
                file.writelines(line)
                file.write('\n')

    def setFrequency(self): 
        delay = 1/ (2 * desiredFrequency) #transfer function to turn input desired frequency into output delay value in ASM file
        return delay

    def start(self):
        os.chdir #how to use this to navigate to ASM_square_wave directory?
        process=subprocess.Popen('make',shell=False,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
        process.wait()

    def stop(self):
        self.p1.terminate()
        #call the assembly file if_GPIO_high?

  # def setFrequency(self,frequency):
      #do something here  

desiredFrequency = 1000 #I guess you can manipulate this?
sqWave = square_wave(desiredFrequency)

sqWave.start()
sqWave.stop()
sqWave.setFrequency(desiredFrequency)
