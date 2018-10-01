import numpy as np
# matrix = map(lambda a:map(int,a.split(",")),raw_input("Enter rows separated by space and within each row elements are separated by comma:").split())
# print matrix

def split(m):
    (r,c) = m.shape
    r = int(r/2)
    c = int(c/2)
    return m[:r,:c],m[:r,c:],m[r:,:c],m[r:,c:]





def strasser(m1,m2):
    if m1.shape == (1,1) or m2.shape == (1,1):
        return m1*m2
    else:
        a11,a12,a21,a22 = split(m1)
        b11,b12,b21,b22 = split(m2)
        M1 = strasser(a11+a22,b11+b22)
        M2 = strasser(a21+a22,b11)
        M3 = strasser(a11,b12-b22)
        M4 = strasser(a22,b21-b11)
        M5 = strasser(a11+a12,b22)
        M6 = strasser(a21-a11,b11+b12)
        M7 = strasser(a12-a22,b21+b22)

        c11 = M1+M4-M5+M7
        c12 = M3+M5
        c21 = M2+M4
        c22 = M1-M2+M3+M6
        return np.vstack((np.hstack((c11,c12)),np.hstack((c21,c22))))
m1 = np.random.random((128,128))
m2 = np.random.random((128,128))
print strasser(m1,m2)
print m1.dot(m2)
print np.allclose(strasser(m1,m2),m1.dot(m2))
