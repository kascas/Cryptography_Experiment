import secrets
import hashlib
import random
import math
import os
from Numtheory import *


def I2OSP(x, xLen):
    if x >= 256 ** xLen:
        print("I2OSP overflow")
        return -1
    base = 256 ** (xLen - 1)
    x_array = bytearray(xLen)
    for i in range(xLen):
        x_array[i] = x // base
        x = x % base
        base = base // 256
    return x_array


def OS2IP(x_array):
    xLen, x, base = len(x_array), 0, 1
    for i in range(xLen):
        x = x + x_array[xLen - 1 - i] * base
        base = base * 256
    return x


def RSAEP(p, n, e):
    if p > n:
        print("RSAEP overflow")
        return -1
    c = FastExp(p, e, n)
    return c


def RSADP(c, n, d):
    if c > n:
        print("RSADP overflow")
        return -1
    m = FastExp(c, d, n)
    return m


def testLen(n):
    k, tmp = 0, 1
    while (n >= tmp):
        k, tmp = k + 1, tmp << 8
    return k


def MGF1(mgfseed, maskLen):
    hLen, T = 20, b''
    if maskLen > (2 ** 32) * hLen:
        print("mask overflow")
        return -1
    counter_max = math.ceil(maskLen / hLen)
    for counter in range(counter_max):
        C = I2OSP(counter, 4)
        T = T + hashlib.sha1(mgfseed + C).digest()
    return T[:maskLen]


def RSAES_OAEP_E(n, e, M, L=b''):
    k, mLen, hLen = testLen(n), len(M), 20

    if len(L) > (2 ** 61 - 1):
        print("label overflow")
        exit(-1)
    if mLen > (k - 2 * hLen - 2):
        print("message overflow")
        exit(-1)
    # EME-OAEP encode
    lHash = hashlib.sha1(L).digest()
    PS = bytearray(k - mLen - 2 * hLen - 2)
    DB = lHash + PS + b'\x01' + M
    seed = bytearray(hLen)
    for i in range(hLen):
        seed[i] = random.randint(1, 255)
    dbMask = MGF1(seed, k - hLen - 1)
    maskedDB = bytearray(k - hLen - 1)
    for i in range(k - hLen - 1):
        maskedDB[i] = DB[i] ^ dbMask[i]
    seedMask = MGF1(maskedDB, hLen)
    maskedSeed = bytearray(hLen)
    for i in range(hLen):
        maskedSeed[i] = seed[i] ^ seedMask[i]
    EM = b'\x00' + maskedSeed + maskedDB
    # RSA encrypt
    m = OS2IP(EM)
    c = RSAEP(m, n, e)
    C = I2OSP(c, k)
    return C


def RSAES_OAEP_D(n, d, C, L=b''):
    k, mLen, hLen = testLen(n), len(C), 20

    if len(L) > (2 ** 61 - 1):
        print("label overflow")
        exit(-1)
    if len(C) != k:
        print("decrypt error")
        exit(-1)
    if k < 2 * hLen + 2:
        print("decrypt error")
        exit(-1)
    # RSA decrypt
    c = OS2IP(C)
    m = RSADP(c, n, d)
    EM = I2OSP(m, k)
    # EME-OAEP decode
    lHash = hashlib.sha1(L).digest()
    Y = EM[0]
    if Y != 0x00:
        print("Y error")
        exit(-1)
    maskedSeed = EM[1:hLen + 1]
    maskedDB = EM[hLen + 1:]
    seedMask = MGF1(maskedDB, hLen)
    seed = bytearray(hLen)
    for i in range(hLen):
        seed[i] = maskedSeed[i] ^ seedMask[i]
    dbMask = MGF1(seed, k - hLen - 1)
    DB = bytearray(k - hLen - 1)
    for i in range(k - hLen - 1):
        DB[i] = maskedDB[i] ^ dbMask[i]
    lHash_d = DB[:hLen]
    if lHash != lHash_d:
        print("label error")
        exit(-1)
    M_pos = 0
    # extract M from DB
    # if the first byte in DB (which doesn't equal '0x00') equals 0x01
    # this byte is the beginning of M
    # else extract M error
    for i in range(hLen, k - hLen - 1):
        if DB[i] != 0x00:
            if DB[i] == 0x01:
                M_pos = i + 1
                break
            else:
                print("extract M error")
                exit(-1)
    M = DB[M_pos:]
    return M
