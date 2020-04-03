import os
from GF_compute import *
from GF_GCD import *


def ByteTransfer(p, total):
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
    array = [[0 for i in range(16)] for j in range(16)]
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


def NrComputer(Nk):
    if Nk == 4:
        return 10
    if Nk == 6:
        return 12
    if Nk == 8:
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
    matrix = [
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2]
    ]
    result = GF_MatrixMulti(matrix, state)
    return result


def AddRoundKey(state, Roundkey):
    # print("state: {}".format(state))
    # print("RoundKey: {}".format(Roundkey))
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


def Key_Sub(w):
    w, w_byte = ((w << 8) & int("0xffffffff", 16)) + (w >> 24), []
    # print("RotWord: {}".format(hex(w)))
    for i in range(4):
        w_byte.append((w >> ((3 - i) * 8)) & int("0xff", 16))
    w_sub = 0
    for i in range(4):
        x, y = w_byte[i] >> 4, w_byte[i] & int("0xf", 16)
        w_byte[i] = S_BOX[x][y]
        w_sub <<= 8
        w_sub += w_byte[i]
    return w_sub


def KeyExpansion(key, Nk, Nr):
    key_word_list = [0 for i in range(Nk)]
    for i in range(Nk):
        key_word_list[i] = (key >> ((Nk - 1 - i) * 32)) & int("0xffffffff", 16)
    matrix = [[0 for i in range(4)] for j in range(4)]
    word_num = 4 * (NrComputer(Nk) + 1)
    w = [0 for i in range(word_num)]
    w[0], w[1], w[2], w[3] = \
        key_word_list[0], key_word_list[1], key_word_list[2], key_word_list[3]
    Rcon = [0 for i in range(14)]
    Rcon[0] = 1
    for i in range(1, 14):
        Rcon[i] = GF_multi(Rcon[i - 1], 2)
    for i in range(4, word_num):
        temp = w[i - 1]
        if i % 4 == 0:
            temp = Key_Sub(w[i - 1]) ^ (Rcon[i // 4 - 1] << 24)
            # print("Rcon: {}".format(hex(Rcon[i // 4 - 1] << 24)))
            # print("Subword: {}".format(hex(Key_Sub(w[i - 1]))))
        w[i] = temp ^ w[i - 4]
        # print("w{}: {}".format(i, hex(w[i]).replace("0x", "").zfill(8)))
    key_array = [[[0 for k in range(4)] for i in range(4)] for j in range(Nr + 1)]
    for i in range(Nr + 1):
        temp = []
        for j in range(4):
            temp.append(ByteTransfer(w[i * 4 + j], 4))
        for j in range(4):
            for k in range(4):
                key_array[i][j][k] = temp[k][j]

    for i in range(Nr + 1):
        print("w{}: ".format(i))
        for j in range(4):
            for k in range(4):
                print(hex(key_array[i][j][k]).replace("0x", ""), end=" ")
            print()

    return key_array


def Text_into_Matrix(s):
    temp, matrix = ByteTransfer(s, 16), [[] for i in range(4)]
    for i in range(16):
        matrix[i % 4].append(temp[i])
    return matrix


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
    result = 0
    for i in range(4):
        for j in range(4):
            result <<= 8
            result += state[j][i]
    return result


if __name__ == "__main__":
    p = int(input("text= "), 16)
    k = int(input("key= "), 16)
    Nk = int(input("keylen= ")) // 32
    print(hex(AES(p, k, 1, Nk)))
