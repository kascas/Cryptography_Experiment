import os
from GF_compute import *
from GF_GCD import *


def ByteTransfer(p, total):
    '''
    this function is used to divide 'int' into bytes
    :param p:
    :param total:
    :return: byte-list
    '''
    # length is the length of p(bits), total is the number of bytes
    List = []
    for i in range(total):
        List.append((p >> ((total - i - 1) * 8)) & int("ff", 16))
    return List


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


def S_BoxCreater():
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


S_BOX = S_BoxCreater()


def NrComputer(Nk):
    '''
    this function is used to compute Nr according to Nk
    :param Nk:
    :return: Nr
    '''
    if Nk == 4:
        return 10
    if Nk == 6:
        return 12
    if Nk == 8:
        return 14


def ShiftRows(state):
    '''
    this function is used to ShiftRows
    :param state:
    :return: ...
    '''
    Nb, move = len(state[0]), [0, 1, 2, 3]
    for i in range(4):
        # temp is the value of the s[i]s[i+4]s[i+8]s[i+12]
        temp = 0
        for j in range(Nb):
            temp <<= 8
            temp += state[i][j]
        for j in range(move[i]):
            temp = ((temp << 8) & ((1 << Nb * 8) - 1)) + (temp >> ((Nb - 1) * 8))
        List = temp.to_bytes(4, 'big')
        for j in range(Nb):
            state[i][j] = List[j]
    return state


def MixColumns(state):
    '''
    this function is used to MixColumns
    :param state:
    :return: ...
    '''
    matrix = [
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2]
    ]
    result = GF_MatrixMulti(matrix, state)
    return result


def AddRoundKey(state, Roundkey):
    '''
    add RoundKey
    :param state:
    :param Roundkey:
    :return: ...
    '''
    for i in range(4):
        for j in range(len(state[0])):
            state[i][j] ^= Roundkey[i][j]
    return state


def SubBytes(state):
    '''
    this function is used to SubBytes
    :param state:
    :return: ...
    '''
    for i in range(len(state)):
        for j in range(len(state[0])):
            x, y = state[i][j] >> 4, state[i][j] & int("0xf", 16)
            state[i][j] = S_BOX[x][y]
    return state


def Key_Sub(w):
    '''
    this function is used to do SubByte to w
    :param w:
    :return: value after sub
    '''
    # left move
    w, w_byte = ((w << 8) & int("0xffffffff", 16)) + (w >> 24), []
    # divide w into 4 bytes
    for i in range(4):
        w_byte.append((w >> ((3 - i) * 8)) & int("0xff", 16))
    w_sub = 0
    # do SubBytes to every w-byte
    for i in range(4):
        x, y = w_byte[i] >> 4, w_byte[i] & int("0xf", 16)
        w_byte[i] = S_BOX[x][y]
        w_sub <<= 8
        w_sub += w_byte[i]
    return w_sub


def KeyExpansion(key, Nk, Nr):
    '''
    this function is used for KeyExpansion
    :param key:
    :param Nk:
    :param Nr:
    :return: a list for key
    '''
    key_word_list = [0 for i in range(Nk)]
    # divide key into words
    for i in range(Nk):
        key_word_list[i] = (key >> ((Nk - 1 - i) * 32)) & int("0xffffffff", 16)
    word_num = 4 * (NrComputer(Nk) + 1)
    # compute Rcon
    Rcon = [0 for i in range(14)]
    Rcon[0] = 1
    for i in range(1, 14):
        Rcon[i] = GF_multi(Rcon[i - 1], 2)
    # compute w[i]
    w = [0 for i in range(word_num)]
    for i in range(Nk):
        w[i] = key_word_list[i]
    for i in range(4, word_num):
        temp = w[i - 1]
        if i % Nk == 0:
            temp = Key_Sub(temp) ^ (Rcon[i // Nk - 1] << 24)
        elif (Nk > 6) and (i % Nk == 4):
            temp = Key_Sub(temp)
        w[i] = temp ^ w[i - Nk]
    # put w into byte-matrix
    key_array = [[[0 for k in range(4)] for i in range(4)] for j in range(Nr + 1)]
    for i in range(Nr + 1):
        temp = []
        for j in range(4):
            temp.append(w[i * 4 + j].to_bytes(4, 'big'))
        for j in range(4):
            for k in range(4):
                key_array[i][j][k] = temp[k][j]
    return key_array


def Text_into_Matrix(s):
    '''
    transfer text into byte-matrix
    :param s:
    :return: a matrix
    '''
    temp, matrix = s.to_bytes(16, 'big'), [[] for i in range(4)]
    for i in range(16):
        matrix[i % 4].append(temp[i])
    return matrix


def Matrix_into_Text(state):
    result = 0
    for i in range(4):
        for j in range(4):
            result <<= 8
            result += state[j][i]
    return result


def AES(s, key, mode, Nk):
    Nr = NrComputer(Nk)
    state = Text_into_Matrix(s)
    key_list = KeyExpansion(key, Nk, Nr)
    state = AddRoundKey(state, key_list[0])
    for i in range(1, Nr):
        state = SubBytes(state)
        state = ShiftRows(state)
        state = MixColumns(state)
        state = AddRoundKey(state, key_list[i])
    state = SubBytes(state)
    state = ShiftRows(state)
    state = AddRoundKey(state, key_list[Nr])
    result = Matrix_into_Text(state)
    return result


if __name__ == "__main__":
    p = int(input("text= "), 16)
    k = int(input("key= "), 16)
    Nk = int(input("keylen= ")) // 32
    print("\n>>>result: " + hex(AES(p, k, 1, Nk)))
