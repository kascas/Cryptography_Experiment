import numpy
from GCD import *

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
    array_det_I = GCD(int(round(numpy.linalg.det(array),0)), 26)[1]
    for i in range(num):
        for j in range(num):
            array_I[i][j] = ((-1) ** (i + j)) * int(round(cofactor_det(array, i, j))) * array_det_I % 26
    return array_I