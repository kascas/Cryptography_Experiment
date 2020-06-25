import secrets
import hashlib
import random
import math
import os


def GCD(a, b):
    # initialize x1,y1,x2,y2
    x1, y1, x2, y2 = 1, 0, 0, 1
    tmpa, tmpb = a, b
    while (1):
        # copy t1,t2 from x2,y2
        t1, t2 = x2, y2
        # recursion equations
        x2, y2 = x1 - (a // b) * x2, y1 - (a // b) * y2
        # exchange values
        x1, y1 = t1, t2
        if (a % b) == 0:
            break
        # exchange values
        a, b = b, a % b
    # if b is negative,make it positive
    if b < 0:
        b, x1, y1 = (-1) * b, (-1) * x1, (-1) * y1
    while (x1 <= 0):
        x1 += tmpb
        y1 -= tmpa
    L = (b, x1, y1)
    return L


def Invert(n, mod):
    g, x, y = GCD(n, mod)
    if g != 1:
        print("gcd != 1, error")
        return -1
    while x <= 0:
        x += mod
        y += n
    return x


def FastExp(x, n, m):
    is_pos = 1
    if n < 0:
        n *= -1
        is_pos = 0
    d = 1
    while n > 0:
        if n & 1:
            d = (d * x) % m
        n >>= 1
        x = (x * x) % m
    if is_pos == 0:
        d = Invert(d, m)
    return d


def Miller_Rabbin(p):
    q, k = p - 1, 0
    # compute k,q s.t. p-1=q*(2^k)
    while q & 1 == 0:
        q >>= 1
        k += 1
    # compute r^q mod p
    for i in range(10):
        j = 0
        r = random.randint(2, p - 1)
        r_q = FastExp(r, q, p)
        if (r_q == 1) or (r_q == p - 1):
            continue
        while j < k:
            if r_q == p - 1:
                break
            r_q = FastExp(r_q, 2, p)
            j += 1
        if j == k and r_q != p - 1:
            return 0
    return 1


def prime_generator(bitlen):
    # 'min' and 'max' is a bitlen-bit random's range
    max = (2 ** bitlen) - 1
    min = 2 ** (bitlen - 1)
    p = 0
    # if p<=min, create a random again
    while (p <= min):
        p = secrets.randbelow(max)
    # find the nearest prime from p. if p isn't a prime, p++
    while (Miller_Rabbin(p) == 0):
        p += 1
    return p


def rsa_init():
    # find two 512-bit random 'p' and 'q'
    # n=p*q is a 1024-bit number
    p = prime_generator(512)
    q = prime_generator(512)
    n, phi_n = p * q, (p - 1) * (q - 1)
    e, gcd, d = p - 1, p - 1, 0
    # select 'e' which is coprime with phi_n
    # select 'd' which is the inverse of e
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
        return -1
    if len(C) != k:
        print("decrypt error")
        return -1
    if k < 2 * hLen + 2:
        print("decrypt error")
        return -1
    # RSA decrypt
    c = OS2IP(C)
    m = RSADP(c, n, d)
    EM = I2OSP(m, k)
    # EME-OAEP decode
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
                return -1
    M = DB[M_pos:]
    return M


if __name__ == "__main__":
    n, e, d = rsa_init()
    M = input("M: ").encode('UTF-8')
    C = RSAES_OAEP_E(n, e, M, b'')
    print('encrypt: {}'.format(C))
    M = RSAES_OAEP_D(n, d, C, b'')
    print('decrypt: {}'.format(M.decode('UTF-8')))
    os.system("pause")
