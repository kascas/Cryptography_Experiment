import os
from DES_3Round import *

IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

IP_I = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

S_BOX = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

E_TRANS = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

P_TRANS = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

P_TRANS_I = [
    9, 17, 23, 31, 13, 28, 2, 18,
    24, 16, 30, 6, 26, 20, 10, 1,
    8, 14, 25, 3, 4, 29, 11, 19,
    32, 12, 22, 7, 5, 27, 15, 21
]

KEY_MOVE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

KEY_TRANS_1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4,
]

KEY_TRANS_2 = [
    14, 17, 11, 24, 1, 5, 3, 28,
    15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56,
    34, 53, 46, 42, 50, 36, 29, 32
]

KEY_TRANS_1_I = [
    8, 16, 24, 56, 52, 44, 36, 0,
    7, 15, 23, 55, 51, 43, 35, 0,
    6, 14, 22, 54, 50, 42, 34, 0,
    5, 13, 21, 53, 49, 41, 33, 0,
    4, 12, 20, 28, 48, 40, 32, 0,
    3, 11, 19, 27, 47, 39, 31, 0,
    2, 10, 18, 26, 46, 38, 30, 0,
    1, 9, 17, 25, 45, 37, 29, 0
]

KEY_TRANS_2_I = [
    5, 24, 7, 16, 6, 10, 20, 18,
    0, 12, 3, 15, 23, 1, 9, 19,
    2, 0, 14, 22, 11, 0, 13, 4,
    0, 17, 21, 8, 47, 31, 27, 48,
    35, 41, 0, 46, 28, 0, 39, 32,
    25, 44, 0, 37, 34, 43, 29, 36,
    38, 45, 33, 26, 42, 0, 30, 40
]


def KeyRestore(key_48, p, c):
    # list1,list2记录两次置换中空缺的位置
    List1, List2 = [], []
    for i in range(64):
        if KEY_TRANS_1_I[i] == 0:
            List1.append(i + 1)
    for i in range(56):
        if KEY_TRANS_2_I[i] == 0:
            List2.append(i + 1)
    # print(List1, List2)
    # 穷举56 bit密钥
    key_56_list = Key56Try(key_48)
    key_56 = Key56Test(key_56_list, p, c)
    # print(key_56)
    key_64 = Key64Creater(key_56)
    return key_64


def Key56Try(key_48):
    key_56, List2, result = 0, [], []
    for i in range(56):
        if KEY_TRANS_2_I[i] == 0:
            List2.append(i + 1)
    for i in range(256):
        temp, key_56 = [0] * 8, 0
        for j in range(8):
            temp[j] = (i >> j) & 1
        # 48-56 bit逆置换，8个空位
        for j in range(56):
            key_56 <<= 1
            if key_48 & (1 << (48 - KEY_TRANS_2_I[j])) != 0:
                key_56 += 1
        # 补空位
        for j in range(8):
            key_56 ^= (temp[j] << (56 - List2[j]))
        # print(bin(key_56).replace("0b","").zfill(56))
        C, D = key_56 >> 28, key_56 & (int("0xfffffff", 16))
        # 循环右移
        for j in range(4):
            C = ((C >> 1) & int("0xfffffff", 16)) + ((C & 1) << 27)
            D = ((D >> 1) & int("0xfffffff", 16)) + ((D & 1) << 27)
        key_56 = (C << 28) + D
        # print(bin(key_56).replace("0b", "").zfill(56))
        result.append(key_56)
    return result


def Key56Test(List, p, c):
    result = 0
    '''
    print("key_56 List: ")
    for i in range(len(List)):
        print(bin(List[i]).replace("0b","").zfill(56))
    '''
    for i in range(len(List)):
        # 取出一个56 bit密钥进行检验
        key_56, key_list, judge = List[i], [], 0
        C, D = key_56 >> 28, key_56 & (int("0xfffffff", 16))
        # 三次循环移位
        for j in range(3):
            for k in range(KEY_MOVE[j]):
                C = ((C << 1) & int("0xfffffff", 16)) + (C >> 27)
                D = ((D << 1) & int("0xfffffff", 16)) + (D >> 27)
            key_56, key_out = (C << 28) + D, 0
            for k in range(48):
                key_out <<= 1
                if key_56 & (1 << (56 - KEY_TRANS_2[k])) != 0:
                    key_out += 1
            key_list.append(key_out)
        for j in range(len(p)):
            if c[j][0] == DES_3Round(p[j][0], key_list) and c[j][1] == DES_3Round(p[j][1], key_list):
                continue
            else:
                judge += 1
        if judge == 0:
            result = List[i]
    # print(bin(result[0]).replace("0b","").zfill(56))
    return result


def Key64Creater(key_56):
    key = 0
    for i in range(64):
        key <<= 1
        if key_56 & (1 << (56 - KEY_TRANS_1_I[i])) != 0:
            key += 1
    for i in range(8):
        temp = (key >> ((7 - i) * 8)) & int("0bff", 16)
        judge, count = 0, 0
        for j in range(7):
            if ((temp >> (j + 1)) & 1) == 1:
                count += 1
        if count % 2 == 0:
            key += 1 << (56 - 8 * i)
    return key


def Diff_Attack(p, c, n):
    # List用于统计最可能的6 bit密钥
    List, key, key_48 = [], [], 0
    # 一共8个S盒
    for i in range(8):
        List.append([])
        # 每个S盒有64种可能的密钥
        List[i] = [0] * 64
    # 一共n组明密文对
    for i in range(n):
        # Test为每组明密文对产生的Test
        Test = OneRound(p[i], c[i])
        # 8个S盒
        for j in range(8):
            for k in range(len(Test[j])):
                List[j][Test[j][k]] += 1
    # print(List)
    for i in range(len(List)):
        max, index = 0, 0
        for j in range(64):
            if List[i][j] >= max:
                index, max = j, List[i][j]
        key.append(index)
    # print(result)
    for i in range(8):
        key_48 = (key_48 << 6) + key[i]
    return key_48, key


def OneRound(p, c):
    '''
    :param p: 两个输入
    :param c: 两个输出
    :return: 一组明密文对产生的8个S盒的Test
    '''
    L0, R0, L3, R3 = [], [], [], []
    for i in range(2):
        L3.append(c[i] >> 32)
        R3.append(c[i] & (int("0xffffffff", 16)))
        L0.append(p[i] >> 32)
        R0.append(p[i] & (int("0xffffffff", 16)))
    E, Ex, Cp = 0, 0, 0
    # E即E(L3)，Ex即E(L3*)
    for i in range(48):
        E <<= 1
        if L3[0] & (1 << (32 - E_TRANS[i])) != 0:
            E += 1
        Ex <<= 1
        if L3[1] & (1 << (32 - E_TRANS[i])) != 0:
            Ex += 1
    # temp即(R3'+L0')
    temp = (R3[0] ^ R3[1]) ^ (L0[0] ^ L0[1])
    for i in range(32):
        Cp <<= 1
        if temp & (1 << (32 - P_TRANS_I[i])) != 0:
            Cp += 1
    '''        
    print(bin(E).replace("0b", "").zfill(48))
    print(bin(Ex).replace("0b", "").zfill(48))
    print(bin(Cp).replace("0b", "").zfill(32))
    '''
    result = []
    for i in range(8):
        E_temp = E >> ((7 - i) * 6) & int("0b111111", 2)
        Ex_temp = Ex >> ((7 - i) * 6) & int("0b111111", 2)
        Cp_temp = Cp >> ((7 - i) * 4) & int("0b1111", 2)
        '''
        print(bin(E_temp).replace("0b", "").zfill(6) + "  " + bin(Ex_temp).replace("0b", "").zfill(6) + "  " + bin(
            Cp_temp).replace("0b", "").zfill(4))
        '''
        Test = TestCreater(E_temp, Ex_temp, Cp_temp, i)
        # print(Test)
        result.append(Test)
    # print(result)
    return result


def TestCreater(E, Ex, Cp, box_num):
    '''
    此函数用于生成Test
    :param E: 输入1
    :param Ex: 输入2
    :param Cp: 输出异或
    :param box_num: S盒编号
    :return: Testj(Ej,Ej*,Cj')
    '''
    List, IN = [], ListCreater(box_num)
    for i in range(len(IN[E ^ Ex][Cp])):
        List.append((IN[E ^ Ex][Cp][i]) ^ E)
    return List


def ListCreater(box_num):
    '''
    此函数用于对每个S盒生成一个“输出异或-可能输入”表
    :param box_num: S盒编号
    :return: 列表（装载8个S盒的表）
    '''
    dic, List = {}, []
    for i in range(64):
        List.append([])
        for j in range(16):
            List[i].append([])
    for i in range(64):
        dic[i] = []
        for j in range(64):
            dic[i].append((j, i ^ j))
    # 64个输入异或
    for i in range(64):
        # 每个输入异或有64个输入对
        for j in range(64):
            result = 0
            # 两次输入
            for k in range(2):
                s_in, s_out = dic[i][j][k], 0
                select = ((s_in >> 5) << 1) + (s_in & 1)
                index = (s_in & int("0b011110", 2)) >> 1
                s_out += S_BOX[box_num][select][index]
                result ^= s_out
            List[i][result].append(dic[i][j][0])
    return List


if __name__ == "__main__":
    c, p = [], []
    n = int(input("how many groups: "))
    for i in range(n):
        c.append([])
        p.append([])
        for j in range(2):
            p_temp = int(input("p{}_{}: ".format(i, j)), 16)
            c_temp = int(input("c{}_{}: ".format(i, j)), 16)
            c[i].append(c_temp)
            p[i].append(p_temp)
    key, key_list = Diff_Attack(p, c, n)
    for i in range(len(key_list)):
        print("J{}= {}".format(i, bin(key_list[i]).replace("0b", "").zfill(6)))
    print("64 bit: ",end="")
    print(hex(KeyRestore(key, p, c)).replace("0x", "").zfill(16))
    os.system("pause")
