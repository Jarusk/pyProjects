from decimal import *
import time
getcontext().prec = 50

def pi_calc(x):
    global pi, a, i
    pi = Decimal(0)
    a = Decimal(1)
    i = 0
    while x > i:
        frac = 4/a
        pi = pi+frac
        i +=1
        a +=2
        print pi
        frac = 4/a
        pi = pi-frac
        i +=1
        a +=2
        print pi

print 'Enter iterations for calculation:'
global x
x = input()
start = time.time()
pi_calc(x)
print ((time.time()-start)/60),'minutes'
    
print 'Press any key to exit:'
raw_input()
