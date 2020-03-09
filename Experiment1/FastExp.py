import os
import time


def FastExp(x, n, m):
    d = 1
    #if n%2==1,compute (d*x)%m,else only do (x*x)%m
    while n > 0:
        if (n % 2) == 1:
            d = (d * x) % m
            n = (n - 1) // 2
        else:
            n = n // 2
        x = (x * x) % m
    return d


x = int(input("x= "))
n = int(input("n= "))
m = int(input("m= "))
# "start" is the moment that FastExp runs
start = time.time()
print("start at {}".format(start))
result = FastExp(x, n, m)
# "end" is the moment that FastExp stops
end = time.time()
print("end at {}".format(start))
print("result= {}".format(result))
print("time from start to end= {} ms".format((end - start) * 1000))
os.system("pause")
