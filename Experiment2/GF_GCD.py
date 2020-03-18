import os
from GF_compute import *


def GF_gcd(a, b):
    if (b == 0):
        return a
    else:
        return GF_gcd(b, GF_div(a, b)[1])


def GF_GCD(a, b):
    if (b == 0):
        return (a, 1, 0)
    else:
        g, x1, y1 = GF_GCD(b, GF_div(a, b)[1])
        x0, y0 = y1, GF_minus(x1, GF_multi(GF_div(a, b)[0], y1))
        return (g, x0, y0)


if __name__ == "__main__":
    a = int(input("input a= "), 16)
    b = int(input("input b= "), 16)
    print("gcd-result is " + str(GF_gcd(a, b)))
    print("GCD-result: g= {}, x= {}, y= {}".format(GF_GCD(a, b)[0], GF_GCD(a, b)[1], GF_GCD(a, b)[2]))
    os.system("pause")
