n = 5
a = [i for i in range(n)]
c = 0
while True:
    print a
    c+=1
    lx = -1
    for i in range(n-1):
        if a[i] < a[i+1]:
            lx = i
    if lx != -1:
        ly = -1
        for i in range(n):
            if a[i] > a[lx]:
                ly = i
        t = a[lx]
        a[lx] = a[ly]
        a[ly] = t
        b = a[lx+1:]
        b = b[::-1]
        a = a[:lx+1]
        a = a+b
    else:
        print "End"
        break
print "Completed"
print c
