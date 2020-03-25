import os
import numpy
from Matrix_I import *


def Hill(c, key):
    key = key.replace("{", "").replace("}", "").split(";")
    n, result = len(key), []
    array = numpy.zeros((n, n), dtype=numpy.int64)
    for i in range(n):
        L = key[i].split(",")
        for j in range(n):
            array[i][j] = L[j]
    group = numpy.zeros((len(c)//n, n), dtype=numpy.int64)
    for i in range(len(c)//n):
        for j in range(n):
            group[i][j] = ord(c[i*n + j]) - ord("a")
    multi = group.dot(array) % 26
    for i in range(len(c)//n):
        for j in range(n):
            result.append(chr(multi[i][j] + ord("a")))
    return "".join(result)


def de_Hill(c, key):
    key = key.replace("{", "").replace("}", "").split(";")
    n, result = len(key), []
    array = numpy.zeros((n, n), dtype=numpy.int64)
    for i in range(n):
        L = key[i].split(",")
        for j in range(n):
            array[i][j] = L[j]
    array_I = matrix_I(array)
    group = numpy.zeros((len(c)//n, n), dtype=numpy.int64)
    for i in range(len(c)//n):
        for j in range(n):
            group[i][j] = ord(c[i*n + j]) - ord("a")
    multi = group.dot(array_I) % 26
    for i in range(len(c)//n):
        for j in range(n):
            result.append(chr(multi[i][j] + ord("a")))
    return "".join(result)


if __name__ == "__main__":
    judge = int(input("please choose [1]crypt, [2]decrypt:  "))
    if (judge == 1):
        c = input("input plaintext: ")
        key = input("input key: ")
        print("result is: " + Hill(c, key))
    else:
        c = input("input text: ")
        key = input("input key: ")
        print("result: " + de_Hill(c, key))
    os.system("pause")
