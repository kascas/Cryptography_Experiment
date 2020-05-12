import secrets
import hashlib
import random
import math
import os
from Numtheory import *


def prime_generator(bitlen):
    max = (2 ** bitlen) - 1
    min = 2 ** (bitlen - 1)
    p = 0
    while (p <= min):
        p = secrets.randbelow(max)
    while (MR_test(p) == 0):
        p += 1
    return p


def rsa_init():
    p = prime_generator(512)
    q = prime_generator(512)
    n, phi_n = p * q, (p - 1) * (q - 1)
    e, gcd, d = p - 1, p - 1, 0
    while (gcd != 1):
        e = secrets.randbelow(phi_n)
        gcd, d, tmp = GCD(e, phi_n)
    if d < 0:
        d += phi_n
    return (n, e, d)


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


def RSASP1(m, n, d):
    if m > n:
        print("RSASP1 overflow")
        return -1
    s = FastExp(m, d, n)
    return s


def RSAVP1(s, n, e):
    if s > n:
        print("RSASP1 overflow")
        return -1
    m = FastExp(s, e, n)
    return m


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
        k, tmp = k + 1, tmp * 256
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
        return -1
    if mLen > (k - 2 * hLen - 2):
        print("message overflow")
        return -1

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

    m = OS2IP(EM)
    c = RSAEP(m, n, e)
    C = I2OSP(c, k)
    return C


def RSAES_OAEP_D(n, d, C, L=b''):
    k, mLen, hLen = testLen(n), len(C), 20

    if len(L) > (2 ** 61 - 1):
        print("label overflow")
        return -1
    if len(C) != k:
        print("decrypt error")
        return -1
    if k < 2 * hLen + 2:
        print("decrypt error")
        return -1

    c = OS2IP(C)
    m = RSADP(c, n, d)
    EM = I2OSP(m, k)

    lHash = hashlib.sha1(L).digest()
    Y = EM[0]
    if Y != 0x00:
        print("Y error")
        return -1
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
        return -1
    M_pos = 0
    for i in range(hLen, k - hLen - 1):
        if DB[i] != 0x00:
            if DB[i] == 0x01:
                M_pos = i + 1
                break
            else:
                print("extract M error")
                return -1
    M = DB[M_pos:]
    return M


if __name__ == "__main__":
    n, e, d = rsa_init()
    print(n, e, d)
    M = b'uweifsauivhssdvadsva'
    C = RSAES_OAEP_E(n, e, M, b'')
    print(C)
    M = RSAES_OAEP_D(n, d, C, b'')
    print(M)
    os.system("pause")
