import math
import os

def Era():
    n = int(input("input n= "))
    L = []
    count = 0
    #put nums from 0 to n into L[]
    for i in range(n + 1):
        L.append(1)
    #test from 2 to sqrt(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        #as for i,if its flag is 1,test it from i^2 to n
        if (L[i] == 1):
            j = i * i
            while (j <= n):
                L[j] = 0
                j += i
    #print all primes
    for i in range(2, n + 1):
        if (L[i] == 1):
            print(i, end="  ")
            count += 1
    #print the number of primes
    print("\ntotal: {}".format(count))


Era()
os.system("pause")
