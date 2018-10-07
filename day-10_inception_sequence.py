# from time import time
def Sieve_of_Eratosthenes(n):
    possible = [[i,True] for i in range(2,n+1)]
    l = len(possible)
    pos = 0
    run = True
    while run:
        cue = possible[pos][0]
        for p in range(pos+cue,l,cue):
            possible[p][1] = False
        run = False
        for i in range(pos+1,l):
            if possible[i][1]:
                pos = i
                run = True
                break
    possible = [p[0] for p in possible if p[1]]
    return possible

# t = time()
prime = Sieve_of_Eratosthenes(int(1e+5))
# print len(primes)
# print "time_taken = {}".format((time() - t)/60)
class Solution:
    def inception(self,i):
        if i == 1:
            return 1
        if i == 2:
            return prime[0]
        else:
            return prime[self.inception(i-1) - 1]
s = Solution()
for i in range(1,10):
    print "inception({}) = {}".format(i,s.inception(i))
        
