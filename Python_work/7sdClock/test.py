from time import sleep
from datetime import datetime
def delay(secs):
    dla = int(secs *2*10**7)
    for i in range(dla):
        pass
# 10000 = 0.000682 seconds
# 20 million = 1 second
d = open("data.txt", "a")
testdur = [10,1,.1,.001]
for i in range(len(testdur)):
    d.write(f"Testing duration of: {testdur[i]} second(s) with delay method\n")
    print(f"Testing {testdur[i]} with delay")
    for j in range(10):
        start = datetime.now()
        delay(testdur[i])
        end = datetime.now()
        starttime = start.minute * 60 + start.second + start.microsecond*pow(10,-6)
        endtime = end.minute * 60 + end.second + end.microsecond*pow(10,-6)
        d.write(f"{endtime - starttime}\n")
# for i in range(len(testdur)):
#     d.write(f"Testing duration of: {testdur[i]} second(s) with sleep method\n")
#     print(f"Testing {testdur[i]} with sleep")
#     for j in range(10):
#         start = datetime.now()
#         sleep(testdur[i])
#         end = datetime.now()
#         starttime = start.minute * 60 + start.second + start.microsecond*pow(10,-6)
#         endtime = end.minute * 60 + end.second + end.microsecond*pow(10,-6)
#         d.write(f"{endtime - starttime}\n")    
print("test complete")    
d.close()
# start = datetime.now()
# delay(.1)
# end = datetime.now()
# starttime = start.minute * 60 + start.second + start.microsecond*pow(10,-6)
# endtime = end.minute * 60 + end.second + end.microsecond*pow(10,-6)
# print(endtime - starttime)