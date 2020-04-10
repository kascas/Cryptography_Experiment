import os
import time
from Sbox import *
from GF_compute import *
from Text_Matrix_Transfer import *

############################################################################################################
# "GFMul{x}(s)" is the function to compute s*x on GF(2^8)                                                  #
# "NrComputer" computes Nr according to Nk                                                                 #
# "Key_Sub" does byte-sub operation to a word of key                                                       #
# "NkJudge" selects the mode from AES-128, AES-192, AES-256 according to the length of key                 #
# There are "AES", "encrypt", "decrypt" for AES:                                                           #
#       "AES(s,key,mode)" has an argument "mode", which selects mode between "encrypt" and "decrypt"       #
#       "encrypt(s,key)" and "decrypt(s,key)" do not have argument "mode", only for encrypt or decrypt     #
#       (They are just two style of programming, nothing different)                                        #
# "SboxCreater" and "Sbox_I_Creater" are in Sbox.py:                                                       #
#       "SboxCreater" computes Sbox                                                                        #
#       "Sbox_I_Creater" computes the inverse of Sbox                                                      #
# "Text_into_Matrix" and "Matrix_into_Text" are in Text_Matrix_Transfer.py:                                #
#       "Text_into_Matrix" stores plaintext or ciphertext into "state"                                     #
#       "Matrix_into_Text" gets plaintext or ciphertext from "state"                                       #
############################################################################################################

S_BOX = SboxCreater()
S_BOX_I = Sbox_I_Creater()
Nb = 4
# compute Rcon
RC = [1 for i in range(14)]
for i in range(1, 14):
    RC[i] = GF_multi(RC[i - 1], 2)


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
        state[1][0], state[1][1], state[1][2], state[1][3] = \
            state[1][1], state[1][2], state[1][3], state[1][0]
        state[2][0], state[2][1], state[2][2], state[2][3] = \
            state[2][2], state[2][3], state[2][0], state[2][1]
        state[3][0], state[3][1], state[3][2], state[3][3] = \
            state[3][3], state[3][0], state[3][1], state[3][2]
    elif mode == 2:
        state[1][0], state[1][1], state[1][2], state[1][3] = \
            state[1][3], state[1][0], state[1][1], state[1][2]
        state[2][0], state[2][1], state[2][2], state[2][3] = \
            state[2][2], state[2][3], state[2][0], state[2][1]
        state[3][0], state[3][1], state[3][2], state[3][3] = \
            state[3][1], state[3][2], state[3][3], state[3][0]
    return state


def MixColumns(state, mode):
    '''
    this function is used to MixColumns
    :param state:
    :return: ...
    '''
    result = [[0 for i in range(4)] for j in range(4)]
    if mode == 1:
        for i in range(4):
            result[0][i] = GFMul2(state[0][i]) ^ GFMul3(state[1][i]) ^ \
                           state[2][i] ^ state[3][i]
            result[1][i] = GFMul2(state[1][i]) ^ GFMul3(state[2][i]) ^ \
                           state[0][i] ^ state[3][i]
            result[2][i] = GFMul2(state[2][i]) ^ GFMul3(state[3][i]) ^ \
                           state[0][i] ^ state[1][i]
            result[3][i] = GFMul2(state[3][i]) ^ GFMul3(state[0][i]) ^ \
                           state[1][i] ^ state[2][i]
    elif mode == 2:
        for i in range(4):
            result[0][i] = GFMul14(state[0][i]) ^ GFMul11(state[1][i]) ^ \
                           GFMul13(state[2][i]) ^ GFMul9(state[3][i])
            result[1][i] = GFMul9(state[0][i]) ^ GFMul14(state[1][i]) ^ \
                           GFMul11(state[2][i]) ^ GFMul13(state[3][i])
            result[2][i] = GFMul13(state[0][i]) ^ GFMul9(state[1][i]) ^ \
                           GFMul14(state[2][i]) ^ GFMul11(state[3][i])
            result[3][i] = GFMul11(state[0][i]) ^ GFMul13(state[1][i]) ^ \
                           GFMul9(state[2][i]) ^ GFMul14(state[3][i])
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
    if mode == 1:
        for i in range(4):
            for j in range(Nb):
                x, y = state[i][j] >> 4, state[i][j] & int("0xf", 16)
                state[i][j] = S_BOX[x][y]
    elif mode == 2:
        for i in range(4):
            for j in range(Nb):
                x, y = state[i][j] >> 4, state[i][j] & int("0xf", 16)
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
    key_word_list, word_num = [0 for i in range(Nk)], Nb * (Nr + 1)
    # divide key into words
    for i in range(Nk):
        key_word_list[i] = (key >> ((Nk - 1 - i) * 32)) & int("0xffffffff", 16)
    # compute w[i]
    w = [0 for i in range(word_num)]
    for i in range(Nk):
        w[i] = key_word_list[i]
    for i in range(Nk, word_num):
        temp = w[i - 1]
        if i % Nk == 0:
            temp = Key_Sub(temp, 0) ^ (RC[i // Nk - 1] << 24)
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


def NkJudge(key):
    Nk = 0
    if len(hex(key).replace("0x", "")) <= 32:
        Nk = 4
    elif len(hex(key).replace("0x", "")) <= 48:
        Nk = 6
    elif len(hex(key).replace("0x", "")) <= 64:
        Nk = 8
    else:
        print("keylen > 256")
        return 0
    return Nk


def AES(s, key, mode):
    Nk = NkJudge(key)
    if Nk == 0:
        return -1
    Nr = NrComputer(Nk)
    state = Text_into_Matrix(s)
    key_list = KeyExpansion(key, Nk, Nr, mode)
    state = AddRoundKey(state, key_list[0], 1)
    for i in range(1, Nr):
        state = SubBytes(state, mode)
        state = ShiftRows(state, mode)
        state = MixColumns(state, mode)
        state = AddRoundKey(state, key_list[i], mode)
    state = SubBytes(state, mode)
    state = ShiftRows(state, mode)
    state = AddRoundKey(state, key_list[Nr], 1)
    result = Matrix_into_Text(state)
    return result


def encrypt(s, key):
    Nk = NkJudge(key)
    if Nk == 0:
        return -1
    Nr = NrComputer(Nk)
    state = Text_into_Matrix(s)
    key_list = KeyExpansion(key, Nk, Nr, 1)
    state = AddRoundKey(state, key_list[0], 1)
    for i in range(1, Nr):
        state = SubBytes(state, 1)
        state = ShiftRows(state, 1)
        state = MixColumns(state, 1)
        state = AddRoundKey(state, key_list[i], 1)
    state = SubBytes(state, 1)
    state = ShiftRows(state, 1)
    state = AddRoundKey(state, key_list[Nr], 1)
    result = Matrix_into_Text(state)
    return result


def decrypt(s, key):
    Nk = NkJudge(key)
    if Nk == 0:
        return -1
    Nr = NrComputer(Nk)
    state = Text_into_Matrix(s)
    key_list = KeyExpansion(key, Nk, Nr, 2)
    state = AddRoundKey(state, key_list[0], 1)
    for i in range(1, Nr):
        state = SubBytes(state, 2)
        state = ShiftRows(state, 2)
        state = MixColumns(state, 2)
        state = AddRoundKey(state, key_list[i], 2)
    state = SubBytes(state, 2)
    state = ShiftRows(state, 2)
    state = AddRoundKey(state, key_list[Nr], 1)
    result = Matrix_into_Text(state)
    return result


if __name__ == "__main__":
    mode = int(input("mode: [1]crypt, [2]decrypt  "))
    p = int(input("text= "), 16)
    k = int(input("key= "), 16)
    start = time.clock()
    c = AES(p, k, mode)
    end = time.clock()
    print("\n>>>result: " + hex(c))
    print("AES took time: {} s".format((end - start)))
    # print("\n\nTest encrypt and decrypt: ")
    # print("encrypt: {}".format(hex(encrypt(p,k))))
    # print("decrypt: {}".format(hex(decrypt(p, k))))
    os.system("pause")
