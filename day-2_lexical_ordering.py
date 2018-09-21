n = 5
a = [i for i in range(n)]
c = 0
while True:
    print a
    c+=1
    #   Finding largest lx such that a[lx] < a[lx+1]
    lx = -1
    for i in range(n-1):
        if a[i] < a[i+1]:
            lx = i
    if lx != -1:
    #   Finding largest ly such that a[ly] > a[lx]
        ly = -1
        for i in range(n):
            if a[i] > a[lx]:
                ly = i
        #   Swap a[lx] and a[ly]
        t = a[lx]
        a[lx] = a[ly]
        a[ly] = t
        #   reversing from a[lx+1] to a[n-1]
        b = a[lx+1:]
        b = b[::-1]
        a = a[:lx+1]
        a = a+b
    else:
        print "End"
        break
print "Completed"
print c
