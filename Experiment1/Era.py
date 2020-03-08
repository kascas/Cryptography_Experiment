import math
import os

def Era():
    n = int(input("input n= "))
    L = []
    count = 0
    for i in range(n + 1):
        L.append(1)
    for i in range(2, int(math.sqrt(n)) + 1):
        if (L[i] == 1):
            j = i * i
            while (j <= n):
                L[j] = 0
                j += i
    for i in range(2, n + 1):
        if (L[i] == 1):
            print(i, end="  ")
            count += 1
    print("\ntotal: {}".format(count))


Era()
os.system("pause")
