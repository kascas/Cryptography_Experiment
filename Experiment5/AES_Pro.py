import os
import time
from Sbox import *
from GF_compute import *
from GF_GCD import *
from GF_Matrix import *
from Text_Matrix_Transfer import *

S_BOX = SboxCreater()
S_BOX_I = Sbox_I_Creater()
Nb = 4


def GFMul2(s):
    result = s << 1
    a7 = result & 0x00000100
    if (a7 != 0):
        result = result & 0x000000ff
        result = result ^ 0x1b
    return result


def GFMul3(s):
    return GFMul2(s) ^ s


def GFMul4(s):
    return GFMul2(GFMul2(s))


def GFMul8(s):
    return GFMul2(GFMul4(s))


def GFMul9(s):
    return GFMul8(s) ^ s


def GFMul11(s):
    return GFMul9(s) ^ GFMul2(s)


def GFMul12(s):
    return GFMul8(s) ^ GFMul4(s)


def GFMul13(s):
    return GFMul12(s) ^ s


def GFMul14(s):
    return GFMul12(s) ^ GFMul2(s)


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


def ShiftRows(state, mode):
    '''
    this function is used to ShiftRows
    :param state:
    :return: ...
    '''
    if mode == 1:
        state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
        state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
        state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]
    elif mode == 2:
        state[1][0], state[1][1], state[1][2], state[1][3] = state[1][3], state[1][0], state[1][1], state[1][2]
        state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
        state[3][0], state[3][1], state[3][2], state[3][3] = state[3][1], state[3][2], state[3][3], state[3][0]
    return state


def MixColumns(state, mode):
    '''
    this function is used to MixColumns
    :param state:
    :return: ...
    '''
    '''
    matrix = []
    if mode == 1:
        matrix = [
            [2, 3, 1, 1],
            [1, 2, 3, 1],
            [1, 1, 2, 3],
            [3, 1, 1, 2]
        ]
    elif mode == 2:
        matrix = [
            [14, 11, 13, 9],
            [9, 14, 11, 13],
            [13, 9, 14, 11],
            [11, 13, 9, 14]
        ]
    result = GF_MatrixMulti(matrix, state)
    '''
    result = [[0 for i in range(4)] for j in range(4)]
    if mode == 1:
        for i in range(4):
            result[0][i] = GF_multi(2, state[0][i]) ^ GF_multi(3, state[1][i]) ^ state[2][i] ^ state[3][i]
            result[1][i] = GF_multi(2, state[1][i]) ^ GF_multi(3, state[2][i]) ^ state[0][i] ^ state[3][i]
            result[2][i] = GF_multi(2, state[2][i]) ^ GF_multi(3, state[3][i]) ^ state[0][i] ^ state[1][i]
            result[3][i] = GF_multi(2, state[3][i]) ^ GF_multi(3, state[0][i]) ^ state[1][i] ^ state[2][i]
    elif mode == 2:
        for i in range(4):
            result[0][i] = GF_multi(14, state[0][i]) ^ GF_multi(11, state[1][i]) ^ \
                           GF_multi(13, state[2][i]) ^ GF_multi(9, state[3][i])
            result[1][i] = GF_multi(9, state[0][i]) ^ GF_multi(14, state[1][i]) ^ \
                           GF_multi(11, state[2][i]) ^ GF_multi(13, state[3][i])
            result[2][i] = GF_multi(13, state[0][i]) ^ GF_multi(9, state[1][i]) ^ \
                           GF_multi(14, state[2][i]) ^ GF_multi(11, state[3][i])
            result[3][i] = GF_multi(11, state[0][i]) ^ GF_multi(13, state[1][i]) ^ \
                           GF_multi(9, state[2][i]) ^ GF_multi(14, state[3][i])
    return result


def AddRoundKey(state, Roundkey, mode):
    '''
    add RoundKey
    :param state:
    :param Roundkey:
    :return: ...
    '''
    if mode == 2:
        Roundkey = MixColumns(Roundkey, 2)
    for i in range(4):
        for j in range(Nb):
            state[i][j] ^= Roundkey[i][j]
    return state


def SubBytes(state, mode):
    '''
    this function is used to SubBytes
    :param state:
    :return: ...
    '''
    for i in range(4):
        for j in range(Nb):
            x, y = state[i][j] >> 4, state[i][j] & int("0xf", 16)
            if mode == 1:
                state[i][j] = S_BOX[x][y]
            elif mode == 2:
                state[i][j] = S_BOX_I[x][y]
    return state


def Key_Sub(w, Nk):
    '''
    this function is used to do SubByte to w
    :param w:
    :return: value after sub
    '''
    # left move
    w_byte = []
    if Nk <= 6:
        w = ((w << 8) & int("0xffffffff", 16)) + (w >> 24)
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


def KeyExpansion(key, Nk, Nr, mode):
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
    word_num = Nb * (Nr + 1)
    # compute Rcon
    Rcon = [0 for i in range(14)]
    Rcon[0] = 1
    for i in range(1, 14):
        Rcon[i] = GF_multi(Rcon[i - 1], 2)
    # compute w[i]
    w = [0 for i in range(word_num)]
    for i in range(Nk):
        w[i] = key_word_list[i]
    for i in range(Nk, word_num):
        temp = w[i - 1]
        if i % Nk == 0:
            temp = Key_Sub(temp, 0) ^ (Rcon[i // Nk - 1] << 24)
        elif (Nk > 6) and (i % Nk == 4):
            temp = Key_Sub(temp, Nk)
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
    if mode == 2:
        key_array.reverse()
    return key_array


def AES(s, key_list, mode, Nk):
    Nr = NrComputer(Nk)
    state = Text_into_Matrix(s)
    state = AddRoundKey(state, key_list[0], 1)
    for i in range(1, Nr):
        start1 = time.clock()
        state = SubBytes(state, mode)
        end1 = time.clock()
        if i == 6:
            print("sub time: {}".format((end1 - start1) * 1000000))
        start2 = time.clock()
        state = ShiftRows(state, mode)
        end2 = time.clock()
        if i == 6:
            print("shift time: {}".format((end2 - start2) * 1000000))
        start3 = time.clock()
        state = MixColumns(state, mode)
        end3 = time.clock()
        if i == 6:
            print("mix time: {}".format((end3 - start3) * 1000000))
        start4 = time.clock()
        state = AddRoundKey(state, key_list[i], mode)
        end4 = time.clock()
        if i == 6:
            print("add time: {}".format((end4 - start4) * 1000000))
    state = SubBytes(state, mode)
    state = ShiftRows(state, mode)
    state = AddRoundKey(state, key_list[Nr], 1)
    result = Matrix_into_Text(state)
    return result


if __name__ == "__main__":
    mode = int(input("mode: [1]crypt, [2]decrypt  "))
    Nk = int(input("keylen= ")) // 32
    p = int(input("text= "), 16)
    k = int(input("key= "), 16)
    key_list = KeyExpansion(k, Nk, NrComputer(Nk), mode)
    print("\n>>>result: " + hex(AES(p, key_list, mode, Nk)))
    os.system("pause")
