from GF_GCD import *


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


def SboxCreater():
    '''
    this function is used to create s-box
    :return: s-box
    '''
    array = [[0 for i in range(16)] for j in range(16)]
    # use GCD to compute inverse
    for x in range(16):
        for y in range(16):
            if x == 0 and y == 0:
                array[x][y] = 0
            else:
                array[x][y] = GF_GCD((x << 4) + y, int("11b", 16))[1]
    matrix = [
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1]
    ]
    c = [
        [1], [1], [0], [0], [0], [1], [1], [0]
    ]
    # use matrix-plus and matrix-multi to compute
    for i in range(16):
        for j in range(16):
            s, s_array = array[i][j], [[0 for i in range(1)] for j in range(8)]
            for k in range(8):
                s_array[k][0] = (s >> k) & 1
            temp, result = GF_MatrixPlus(GF_MatrixMulti(matrix, s_array), c), 0
            for k in range(8):
                result <<= 1
                result = result + temp[7 - k][0]
            array[i][j] = result
    return array


def Sbox_I_Creater():
    array = [[0 for i in range(16)] for j in range(16)]
    for x in range(16):
        for y in range(16):
            array[x][y] = (x << 4) + y
    matrix = [
        [0, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 1, 0]
    ]
    c = [
        [1], [0], [1], [0], [0], [0], [0], [0]
    ]
    # use matrix-plus and matrix-multi to compute
    for i in range(16):
        for j in range(16):
            s, s_array = array[i][j], [[0 for i in range(1)] for j in range(8)]
            for k in range(8):
                s_array[k][0] = (s >> k) & 1
            temp, result = GF_MatrixPlus(GF_MatrixMulti(matrix, s_array), c), 0
            for k in range(8):
                result <<= 1
                result = result + temp[7 - k][0]
            array[i][j] = result
    # use GCD to compute inverse
    for x in range(16):
        for y in range(16):
            if array[x][y] == 0:
                array[x][y] = 0
            else:
                array[x][y] = GF_GCD(array[x][y], int("11b", 16))[1]
    return array
