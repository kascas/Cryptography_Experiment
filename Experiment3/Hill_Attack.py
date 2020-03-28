import os
import numpy
from Matrix_I import *
from GCD import *


def One_mark(n):
    count, L, move = 0, [], 0
    while (n != 0):
        if n & 1 == 1:
            count += 1
            L.append(move)
        n, move = n >> 1, move + 1
    return (count, L)


def Hill_Attack(c, m, dim):
    c_array_temp = numpy.zeros((len(c) // dim, dim), dtype=numpy.int64)
    m_array_temp = numpy.zeros((len(c) // dim, dim), dtype=numpy.int64)
    for i in range(len(c) // dim):
        for j in range(dim):
            c_array_temp[i][j], m_array_temp[i][j] = ord(c[dim * i + j]) - ord("a"), ord(m[dim * i + j]) - ord("a")
    c_array = numpy.zeros((dim, dim), dtype=numpy.int64)
    m_array = numpy.zeros((dim, dim), dtype=numpy.int64)
    c_array[:, :], m_array[:, :] = c_array_temp[0:dim, :], m_array_temp[0:dim, :]
    max, current = 1 << (len(c) // dim), 2
    while GCD(int(round(numpy.linalg.det(c_array))), 26)[0] != 1:
        while (One_mark(current)[0] != dim):
            current += 1
        if (current >= max):
            return "Error, cannot decrypt"
        L = One_mark(current)[1]
        for i in range(dim):
            c_array[i, :] = c_array_temp[L[i], :]
            m_array[i, :] = m_array_temp[L[i], :]
        current += 1
    c_array_I = matrix_I(c_array)
    return c_array_I.dot(m_array) % 26


if __name__ == "__main__":
    c = input("input plaintext: ")
    m = input("input ciphertext: ")
    dim = int(input("input dimension: "))
    print(Hill_Attack(c, m, dim))
    os.system("pause")
