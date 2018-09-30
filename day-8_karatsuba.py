import numpy as np
from time import time

B = 10
m = 7

def karatsuba(a,b):
    sa = str(a)
    sb = str(b)
    if len(sa) <= 10 or len(sb) <= 10:
        return a*b
    else:
        a1,a0 = int(sa[:len(sa)-m]),int(sa[len(sa)-m:])
        b1,b0 = int(sb[:len(sb)-m]),int(sb[len(sb)-m:])
        z2 = karatsuba(a1,b1)
        z0 = karatsuba(a0,b0)
        z1 = (a0 - a1)*(b1 - b0) + z2 + z0
        return z2*(B**(2*m)) + z1*(B**m) + z0

a = int(raw_input("Enter A:"))
b = int(raw_input("Enter B:"))
polarity = -1 if a<0 or b < 0 else 1
a,b = abs(a),abs(b)
print karatsuba(a,b)*polarity
