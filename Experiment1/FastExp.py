import os


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
result = FastExp(x, n, m)
print("result= {}".format(result))
os.system("pause")
