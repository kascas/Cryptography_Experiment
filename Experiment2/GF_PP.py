import os
from GF_compute import *


def GF_PP(n=8):
    max, count, L = 0, 0, []
    for i in range(n + 1):
        max += (1 << i)
    # 遍历
    for i in range((1 << n), max):
        judge = False
        # 判断是否可约
        for j in range(2, (1 << n // 2 + 1)):
            if GF_div(i, j)[1] == 0:
                judge = True
                break
        if judge:
            continue
        # 如果不可约则判断整除
        m = 2 ** n - 1
        # 如果整除x^m+1
        if GF_div((1 << m) + 1, i)[1] != 0:
            continue
        # 判断是否整除x^q+1
        for q in range(1, m):
            k = (1 << q) + 1
            if GF_div(k, i)[1] == 0:
                judge = True
                break
        if judge:
            continue
        else:
            count += 1
            L.append(i)
    return (L, count)


if __name__ == "__main__":
    n = int(input("input n= "))
    L, count = GF_PP(n)
    print(L)
    print("result: {}".format(count))
