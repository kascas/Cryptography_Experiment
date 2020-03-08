import os
import time


def FastExp(x, n, m):
    d = 1
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
start = time.time()
print("start at {}".format(start))
result = FastExp(x, n, m)
end = time.time()
print("end at {}".format(start))
print("result= {}".format(result))
print("time from start to end= {} ms".format((end - start) * 1000))
os.system("pause")
