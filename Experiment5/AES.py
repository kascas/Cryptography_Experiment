import os
import numpy as np
from GF_compute import *
from GF_GCD import *


def ByteTransfer(p, total):
    # length is the length of p(bits), total is the number of bytes
    List = []
    for i in range(total):
        List.append((p >> ((total - i - 1) * 8)) & int("ff", 16))
    return List


def GF_MatrixMulti(a, b):
    result = np.zeros((len(a), len(b[0])), dtype=np.int64)
    for i in range(len(a)):
        for j in range(len(b[0])):
            temp = 0
            for k in range(len(a[0])):
                temp = GF_plus(temp, GF_multi(a[i][k], b[k][j]))
            result[i][j] = temp
    return result


def GF_MatrixPlus(a, b):
    result = np.zeros((len(a), len(a[0])), dtype=np.int64)
    for i in range(len(a)):
        for j in range(len(a[0])):
            result[i][j] = GF_plus(a[i][j], b[i][j])
    return result


def S_BoxCreater():
    array = np.zeros((16, 16), dtype=np.int64)
    for x in range(16):
        for y in range(16):
            if x == 0 and y == 0:
                array[x][y] = 0
            else:
                array[x][y] = GF_GCD((x << 4) + y, int("11b", 16))[1]
    matrix = np.array([
        [1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 1]
    ])
    c = np.array([
        [1], [1], [0], [0], [0], [1], [1], [0]
    ])
    for i in range(16):
        for j in range(16):
            s, s_array = array[i][j], np.zeros((8, 1), dtype=np.int64)
            for k in range(8):
                s_array[k][0] = (s >> k) & 1
            temp, result = GF_MatrixPlus(GF_MatrixMulti(matrix, s_array), c), 0
            for k in range(8):
                result <<= 1
                result = result + temp[7 - k]
            array[i][j] = result
    # test module
    '''
    for i in range(16):
        for j in range(16):
            print(hex(array[i][j]).replace("0x", "").zfill(2) + " ", end="")
            if j == 15:
                print()
    '''
    return array


S_BOX = S_BoxCreater()


def NrComputer(Nb, Nk):
    if Nb == 4 and Nk == 4:
        return 10
    if (Nb == 6 and Nk == 4) \
            or (Nb == 6 and Nk == 6) \
            or (Nb == 4 and Nk == 6):
        return 12
    if (Nb == 8 and Nk == 4) \
            or (Nb == 8 and Nk == 6) \
            or (Nb == 8 and Nk == 8) \
            or (Nb == 6 and Nk == 8) \
            or (Nb == 4 and Nk == 8):
        return 14


def ShiftRows(state):
    Nb, move = len(state[0]), [0, 1, 2, 3]
    result = [[0 for i in range(Nb)] for j in range(4)]
    for i in range(4):
        temp = 0
        for j in range(Nb):
            temp <<= 8
            temp += state[i][j]
        for j in range(move[i]):
            temp = ((temp << 8) & ((1 << Nb * 8) - 1)) + (temp >> ((Nb - 1) * 8))
        List = ByteTransfer(temp, Nb)
        for j in range(Nb):
            state[i][j] = List[j]
    return state


def MixColumns(state):
    matrix = np.array([
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2]
    ])
    result = GF_MatrixMulti(matrix, state)
    return result


def AddRoundKey(state, Roundkey):
    for i in range(4):
        for j in range(len(state[0])):
            state[i][j] ^= Roundkey[i][j]
    return state


def SubBytes(state):
    for i in range(len(state)):
        for j in range(len(state[0])):
            x, y = state[i][j] >> 4, state[i][j] & int("0xf", 16)
            state[i][j] = S_BOX[x][y]
    return state

def

def AES(state, key, mode, Nb, Nk):
    key_list = KeyExpansion(key)
    state = AddRoundKey(state, key_list[0])
    Nr = NrComputer(Nb, Nk)
    for i in range(Nr - 1):
        state = SubBytes(state)
        state = ShiftRows(state)
        state = MixColumns(state)
        AddRoundKey(state, key_list[i + 1])
    state = SubBytes(state)
    state = ShiftRows(state)
    state = AddRoundKey(state, key_list[Nr])
    return state


if __name__ == "__main__":
    List = ByteTransfer(int("2b24424b9fed5966", 16), 8)
    for i in range(8):
        print(hex(List[i]))
    print(S_BOX)
    a = [
        [7, 4, 1, 2],
        [5, 3, 2, 7],
        [8, 4, 2, 1],
        [5, 4, 2, 1]
    ]
    b = [
        [int("87", 16), int("f2", 16), int("4d", 16), int("97", 16)],
        [int("6e", 16), int("4c", 16), int("90", 16), int("ec", 16)],
        [int("46", 16), int("e7", 16), int("4a", 16), int("c3", 16)],
        [int("a6", 16), int("8c", 16), int("d8", 16), int("95", 16)],
    ]
    print(ShiftRows(a))
    print(MixColumns(b))
