from GF_compute import *


def GF_MatrixMulti(a, b):
    result = [[0 for i in range(len(b[0]))] for j in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            temp = 0
            for k in range(len(a[0])):
                temp = GF_plus(temp, GF_multi(a[i][k], b[k][j]))
            result[i][j] = temp
    return result


def GF_MatrixPlus(a, b):
    result = [[0 for i in range(len(a[0]))] for j in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a[0])):
            result[i][j] = GF_plus(a[i][j], b[i][j])
    return result
