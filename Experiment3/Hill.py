import os
import numpy
from GCD import GCD


def Hill(c, key):
    key = key.replace("{", "").replace("}", "").split(";")
    n, result = len(key), []
    array = numpy.zeros((n, n), dtype=numpy.int64)
    for i in range(n):
        L = key[i].split(",")
        for j in range(n):
            array[i][j] = L[j]
    for i in range(0, len(c), n):
        group = numpy.zeros((1, n), dtype=numpy.int64)
        for j in range(n):
            group[0][j] = ord(c[i + j]) - ord("a")
        multi = group.dot(array) % 26
        for j in range(n):
            result.append(chr(multi[0][j] + ord("a")))
    return "".join(result)


def cofactor_det(array, row, line):
    num = len(array)
    result = numpy.zeros((num - 1, num - 1), dtype=numpy.int64)
    result_row, result_line = 0, 0
    for i in range(num):
        if (i == line):
            continue
        result_line = 0
        for j in range(num):
            if (j == row):
                continue
            result[result_row][result_line] = array[i][j]
            result_line += 1
        result_row += 1
    return numpy.linalg.det(result)


def matrix_I(array, n=26):
    num = len(array)
    array_I = numpy.zeros((num, num), dtype=numpy.int64)
    array_det_I = GCD(int(round(numpy.linalg.det(array))), 26)[1]
    for i in range(num):
        for j in range(num):
            array_I[i][j] = ((-1) ** (i + j)) * int(round(cofactor_det(array, i, j))) * array_det_I % 26
    return array_I


def de_Hill(c, key):
    key = key.replace("{", "").replace("}", "").split(";")
    n, result = len(key), []
    array = numpy.zeros((n, n), dtype=numpy.int64)
    for i in range(n):
        L = key[i].split(",")
        for j in range(n):
            array[i][j] = L[j]
    array_I = matrix_I(array)
    for i in range(0, len(c), n):
        group = numpy.zeros((1, n), dtype=numpy.int64)
        for j in range(n):
            group[0][j] = ord(c[i + j]) - ord("a")
        multi = group.dot(array_I) % 26
        for j in range(n):
            result.append(chr(multi[0][j] + ord("a")))
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
