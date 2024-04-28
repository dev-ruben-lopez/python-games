import time
import sys


tms = 0.1
curr = time.perf_counter()
res = 0


while res < 10:
    now = time.perf_counter()
    if ( (now - curr) >= tms ):
        print ("Yes..." + str(now))
        curr = now
        res += 1
       
    