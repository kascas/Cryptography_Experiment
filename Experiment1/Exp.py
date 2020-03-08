import os
import time


def Exp(x, n, m):
    result = 1
    for i in range(n):
        result = (result * x) % m
    return result


x = int(input("x= "))
n = int(input("n= "))
m = int(input("m= "))
start = time.time()
print("start at {}".format(start))
result = Exp(x, n, m)
end = time.time()
print("end at {}".format(end))
print("result= {}".format(result))
print("time from start to end= {} ms".format((end - start) * 1000))
os.system("pause")
