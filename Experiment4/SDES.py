import os

IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_I = [4, 1, 3, 5, 7, 2, 8, 6]
E_TRANS = [4, 1, 2, 3, 2, 3, 4, 1]
S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]
S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]
P_TRANS = [2, 4, 3, 1]
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
KEY_MOVE = [1, 2]


def SDES(p, key, mode):
    p_IP, p_IP_I = 0, 0
    # e_trans
    p_IP = IP_Trans(p)
    # print("IP(p): " + hex(p_IP))
    # divide p into L and R
    L, R = p_IP >> 4, p_IP & (int("0xf", 16))
    # print("L0: " + hex(L))
    # print("R0: " + hex(R))
    # create key_list
    key_list = KeyCreater(key, mode)
    # feistel strcture
    for i in range(2):
        L, R = R, Function(R, key_list[i]) ^ L
    p = (R << 4) + L
    p_IP_I = IP_I_Trans(p)
    # print("IP_I(p): ", hex(p_IP_I).zfill(2))
    return p_IP_I


def Function(R, key):
    R_E, R_P = 0, 0
    # e_trans
    R_E = E_Trans(R) ^ key
    # s_in is a 48-bit input, extract is used to divide s_in into 8 4-bit pieces
    # s_box
    s0, s1 = R_E >> 4, R_E & int("0xf", 16)
    s0_x, s0_y = ((s0 >> 3) << 1) + (s0 & 1), (((s0 >> 2) & 1) << 1) + ((s0 >> 1) & 1)
    s1_x, s1_y = ((s1 >> 3) << 1) + (s1 & 1), (((s1 >> 2) & 1) << 1) + ((s1 >> 1) & 1)
    s_out = (S0[s0_x][s0_y] << 2) + S1[s1_x][s1_y]
    # p_trans
    R_P = P_Trans(s_out)
    return R_P


def KeyCreater(key, mode):
    key_list, key_in = [], 0
    key_in = PC_1(key)
    # divide key_in into C and D
    C, D = key_in >> 5, key_in & (int("0x1f", 16))
    for i in range(2):
        # left move
        C, D = KeyMove(C, D, i)
        key, key_out = (C << 5) + D, 0
        # key_trans_2
        key_out = PC_2(key)
        key_list.append(key_out)
    if mode == 2:
        key_list.reverse()
    return key_list


def KeyMove(C, D, i):
    for j in range(KEY_MOVE[i]):
        C = ((C << 1) & int("0x1f", 16)) + (C >> 4)
        D = ((D << 1) & int("0x1f", 16)) + (D >> 4)
    return C, D


def PC_1(key):
    key_in = 0
    # key_trans_1
    for i in range(10):
        key_in <<= 1
        if key & (1 << (10 - P10[i])) != 0:
            key_in += 1
    return key_in


def PC_2(key):
    key_out = 0
    for k in range(8):
        key_out <<= 1
        if key & (1 << (10 - P8[k])) != 0:
            key_out += 1
    return key_out


def IP_Trans(p):
    p_IP = 0
    # e_trans
    for i in range(8):
        p_IP <<= 1
        if p & (1 << (8 - IP[i])) != 0:
            p_IP += 1
    return p_IP


def IP_I_Trans(p):
    p_IP_I = 0
    for i in range(8):
        p_IP_I <<= 1
        if p & (1 << (8 - IP_I[i])) != 0:
            p_IP_I += 1
    return p_IP_I


def E_Trans(R):
    R_E = 0
    # e_trans
    for i in range(8):
        R_E <<= 1
        if R & (1 << (4 - E_TRANS[i])) != 0:
            R_E += 1
    return R_E


def P_Trans(s_out):
    R_P = 0
    for i in range(4):
        R_P <<= 1
        if s_out & (1 << (4 - P_TRANS[i])) != 0:
            R_P += 1
    return R_P


if __name__ == "__main__":
    mode = int(input("mode: [1]crypt [2]decrypt "))
    p = int(input("input text: "), 16)
    key = int(input("input key: "), 16)
    print("\nciphertext is: {}".format(hex(SDES(p, key, mode))))
    os.system("pause")
