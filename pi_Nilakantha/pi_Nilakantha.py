from decimal import *
import time
getcontext().prec = 50

def pi_calc(x):
    global pi, a, b, c, i
    pi = Decimal(3)
    a = Decimal(2)
    b = Decimal(3)
    c = Decimal(4)
    i = 0
    while x > i:
        frac = 4/(a*b*c)
        pi = pi+frac
        i +=1
        a +=2
        b +=2
        c +=2
        print pi
        frac = 4/(a*b*c)
        pi = pi-frac
        i +=1
        a +=2
        b +=2
        c +=2
        print pi

print 'Enter iterations for calculation:'
global x
x = input()
start = time.time()
pi_calc(x)
print ((time.time()-start)/60),'minutes'
    
print 'Press any key to exit:'
raw_input()
