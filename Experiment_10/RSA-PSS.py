import secrets
import hashlib
import random
import math
import os
from Numtheory import *

hLen = 20
sLen = 20
padding1 = b'\x00\x00\x00\x00\x00\x00\x00\x00'


def rsa_init():
    # find two 512-bit random 'p' and 'q'
    # n=p*q is a 1024-bit number
    p = prime(512)
    q = prime(512)
    n, phi_n = p * q, (p - 1) * (q - 1)
    e, gcd, d = p - 1, p - 1, 0
    # select 'e' which is coprime with phi_n
    # select 'd' which is the inverse of e
    while (gcd != 1):
        e = secrets.randbelow(phi_n)
        gcd, d, tmp = GCD(e, phi_n)
    if d < 0:
        d += phi_n
    return ((n, e), (n, d))


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


def BytelenTest(n):
    length = 0
    while (n != 0):
        n >>= 8
        length += 1
    return length


def BitlenTest(n):
    length = 0
    while (n != 0):
        n >>= 1
        length += 1
    return length


def PSS_encode(M, emBits):
    emLen = math.ceil(emBits / 8)
    salt = bytearray(sLen)
    padding2 = bytearray(emLen - sLen - hLen - 1)
    maskedDB = bytearray(emLen - hLen - 1)

    mHash = hashlib.sha1(M).digest()
    for i in range(sLen):
        salt[i] = secrets.randbelow(256)
    Mp = padding1 + mHash + salt
    H = hashlib.sha1(Mp).digest()
    for i in range(emLen - sLen - hLen - 2):
        padding2[i] = 0
    padding2[-1] = 1
    DB = padding2 + salt
    dbMask = MGF1(H, emLen - hLen - 1)
    for i in range(len(DB)):
        maskedDB[i] = dbMask[i] ^ DB[i]
    tmp = (1 << (8 - 8 * emLen + emBits)) - 1
    maskedDB[0] = maskedDB[0] & tmp
    EM = maskedDB + H + b'\xbc'

    return EM


def PSS_verify(M, EM, emBits):
    mHash = hashlib.sha1(M).digest()
    emLen = math.ceil(emBits / 8)
    if EM[-1] != 0xbc:
        return -1
    maskedDB = EM[:emLen - hLen - 1]
    H = EM[emLen - hLen - 1:-1]
    tmp = (~((1 << (8 - 8 * emLen + emBits)) - 1)) & 0xff
    if maskedDB[0] & tmp != 0:
        return -1
    dbMask = MGF1(H, emLen - hLen - 1)
    DB = bytearray(emLen - hLen - 1)
    for i in range(emLen - hLen - 1):
        DB[i] = maskedDB[i] ^ dbMask[i]
    tmp = (1 << (8 - 8 * emLen + emBits)) - 1
    DB[0] = DB[0] & tmp
    for i in range(emLen - hLen - sLen - 2):
        if DB[i] != 0:
            return -1
    if DB[emLen - hLen - sLen - 2] != 0x01:
        return -1
    salt = DB[emLen - hLen - sLen - 1:]
    Mp = padding1 + mHash + salt
    Hp = hashlib.sha1(Mp).digest()
    if Hp != H:
        return -1
    return 1


def RSA_sign(pr, M):
    n, d = pr
    modBits = BitlenTest(n)
    emLen = math.ceil((modBits - 1) / 8)
    k = BytelenTest(n)
    EM = PSS_encode(M, modBits - 1)
    m = OS2IP(EM)
    s = RSASP1(m, n, d)
    S = I2OSP(s, k)
    return S


def RSA_verify(pu, M, S):
    n, e = pu
    modBits = BitlenTest(n)
    emLen = math.ceil((modBits - 1) / 8)
    k = BytelenTest(n)
    s = OS2IP(S)
    m = RSAVP1(s, n, e)
    EM = I2OSP(m, emLen)
    return PSS_verify(M, EM, modBits - 1)


if __name__ == "__main__":
    pu, pr = rsa_init()
    print("public  key: {}".format(pu))
    print("private key: {}".format(pr))
    M = input("M: ").encode('UTF-8')
    S = RSA_sign(pr, M)
    print("verify: {}".format(RSA_verify(pu, M, S)))
    os.system("pause")
