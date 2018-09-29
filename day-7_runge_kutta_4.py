from math import sqrt
original = lambda x:(1/16.0)*(x**2 + 4)**2
function = lambda x,y: x*sqrt(y)

h = 0.1
xn = 0.0
yn = 1.0

def RK4(h,x,y):
    k1 = h*function(x,y)
    k2 = h*function(x+(h/2.0),y+(k1/2.0))
    k3 = h*function(x+(h/2.0),y+(k2/2.0))
    k4 = h*function(x+h,y+k3)
    return y + (1/6.0)*(k1 + 2.0*(k2+k3) + k4)

target_x = 10.0
x_s = []
y_s = []
while xn < target_x:
    x_s.append(xn)
    y_s.append(yn)
    y_next = RK4(h,xn,yn)
    xn += h
    yn = y_next
for x,y in zip(x_s[::10],y_s[::10]):
    o_y = original(x)
    print("x : {}; RK4 : {:.3f}; Original : {:.3f}; Error : {};".format(x,y,o_y,o_y - y))
