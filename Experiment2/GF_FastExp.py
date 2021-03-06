import os
from GF_compute import *


def GF_Exp(x, b, n=int("0b100011011", 2)):
    result = 1
    for i in range(b):
        result = GF_multi(result, x)
    return result


def GF_FastExp(x, b, n=int("0b100011011", 2)):
    result = 1
    while (b > 0):
        if b & 1:
            result = GF_multi(result, x)
        b >>= 1
        x = GF_multi(x, x)
    return result


if __name__ == "__main__":
    x_temp, type = input("input x and its type= ").split()
    x = trans(x_temp, type)
    b_temp, type = input("input b and its type= ").split()
    b = trans(b_temp, type)
    print("FastExp-result is " + str(GF_FastExp(x, b)))
    print("Exp-result is " + str(GF_Exp(x, b)))
    os.system("pause")
