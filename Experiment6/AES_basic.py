import os
import time

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


S_BOX = [
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16],
]

S_BOX_I = [
    [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
    [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
    [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
    [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
    [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
    [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
    [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
    [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
    [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
    [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
    [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
    [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
    [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
    [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
    [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
    [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]

]

Nb = 4

RC = [
    0x1, 0x2, 0x4, 0x8, 0x10, 0x20, 0x40,
    0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d
]


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
    if Nk == 4:
        return 10
    if Nk == 6:
        return 12
    if Nk == 8:
        return 14


def ShiftRows(state):
    state[1][0], state[1][1], state[1][2], state[1][3] = \
        state[1][1], state[1][2], state[1][3], state[1][0]
    state[2][0], state[2][1], state[2][2], state[2][3] = \
        state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = \
        state[3][3], state[3][0], state[3][1], state[3][2]
    return state


def InvShiftRows(state):
    state[1][0], state[1][1], state[1][2], state[1][3] = \
        state[1][3], state[1][0], state[1][1], state[1][2]
    state[2][0], state[2][1], state[2][2], state[2][3] = \
        state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = \
        state[3][1], state[3][2], state[3][3], state[3][0]
    return state


def MixColumns(state):
    result = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        result[0][i] = GFMul2(state[0][i]) ^ GFMul3(state[1][i]) ^ \
                       state[2][i] ^ state[3][i]
        result[1][i] = GFMul2(state[1][i]) ^ GFMul3(state[2][i]) ^ \
                       state[0][i] ^ state[3][i]
        result[2][i] = GFMul2(state[2][i]) ^ GFMul3(state[3][i]) ^ \
                       state[0][i] ^ state[1][i]
        result[3][i] = GFMul2(state[3][i]) ^ GFMul3(state[0][i]) ^ \
                       state[1][i] ^ state[2][i]
    return result


def InvMixColumns(state):
    result = [[0 for i in range(4)] for j in range(4)]
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


def AddRoundKey(state, Roundkey):
    for i in range(4):
        for j in range(Nb):
            state[i][j] ^= Roundkey[i][j]
    return state


def InvAddRoundKey(state, Roundkey):
    Roundkey = InvMixColumns(Roundkey)
    for i in range(4):
        for j in range(Nb):
            state[i][j] ^= Roundkey[i][j]
    return state


def SubBytes(state):
    for i in range(4):
        for j in range(Nb):
            x, y = state[i][j] >> 4, state[i][j] & int("0xf", 16)
            state[i][j] = S_BOX[x][y]
    return state


def InvSubBytes(state):
    for i in range(4):
        for j in range(Nb):
            x, y = state[i][j] >> 4, state[i][j] & int("0xf", 16)
            state[i][j] = S_BOX_I[x][y]
    return state


def RotWord(w):
    return ((w << 8) & int("0xffffffff", 16)) + (w >> 24)


def Key_Sub(w):
    w_byte = []
    for i in range(4):
        w_byte.append((w >> ((3 - i) * 8)) & int("0xff", 16))
    w_sub = 0
    for i in range(4):
        x, y = w_byte[i] >> 4, w_byte[i] & int("0xf", 16)
        w_byte[i] = S_BOX[x][y]
        w_sub <<= 8
        w_sub += w_byte[i]
    return w_sub


def KeyExpansion(key, Nk, Nr, mode):
    key_word_list, word_num = [0 for i in range(Nk)], Nb * (Nr + 1)
    for i in range(Nk):
        key_word_list[i] = (key >> ((Nk - 1 - i) * 32)) & int("0xffffffff", 16)
    w = [0 for i in range(word_num)]
    for i in range(Nk):
        w[i] = key_word_list[i]
    for i in range(Nk, word_num):
        temp = w[i - 1]
        if i % Nk == 0:
            temp = Key_Sub(RotWord(temp)) ^ (RC[i // Nk - 1] << 24)
        elif (Nk > 6) and (i % Nk == 4):
            temp = Key_Sub(temp)
        w[i] = temp ^ w[i - Nk]
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


def Text_to_State(s):
    temp, matrix = s.to_bytes(16, 'big'), [[] for i in range(4)]
    for i in range(16):
        matrix[i % 4].append(temp[i])
    return matrix


def State_to_Text(state):
    result = 0
    for i in range(4):
        for j in range(4):
            result <<= 8
            result += state[j][i]
    return result


def encrypt(s, key):
    Nk = NkJudge(key)
    if Nk == 0:
        return -1
    Nr = NrComputer(Nk)
    state = Text_to_State(s)
    key_list = KeyExpansion(key, Nk, Nr, 1)
    state = AddRoundKey(state, key_list[0])
    for i in range(1, Nr):
        state = SubBytes(state)
        state = ShiftRows(state)
        state = MixColumns(state)
        state = AddRoundKey(state, key_list[i])
    state = SubBytes(state)
    state = ShiftRows(state)
    state = AddRoundKey(state, key_list[Nr])
    result = State_to_Text(state)
    return result


def decrypt(s, key):
    Nk = NkJudge(key)
    if Nk == 0:
        return -1
    Nr = NrComputer(Nk)
    state = Text_to_State(s)
    key_list = KeyExpansion(key, Nk, Nr, 2)
    state = AddRoundKey(state, key_list[0])
    for i in range(1, Nr):
        state = InvSubBytes(state)
        state = InvShiftRows(state)
        state = InvMixColumns(state)
        state = InvAddRoundKey(state, key_list[i])
    state = InvSubBytes(state)
    state = InvShiftRows(state)
    state = AddRoundKey(state, key_list[Nr])
    result = State_to_Text(state)
    return result


if __name__ == "__main__":
    mode = int(input("mode: [1]crypt, [2]decrypt  "))
    p = int(input("text= "), 16)
    k = int(input("key= "), 16)
    c, start, end = 0, 0, 0
    if mode == 1:
        start = time.perf_counter()
        for i in range(10000):
            c = encrypt(p, k)
        end = time.perf_counter()
    else:
        start = time.perf_counter()
        for i in range(10000):
            c = decrypt(p, k)
        end = time.perf_counter()
    print("\n>>>result: " + hex(c))
    print("AES took time: {} s".format((end - start)))
    os.system("pause")
