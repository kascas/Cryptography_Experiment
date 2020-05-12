import secrets
import os
import time
from Numtheory import *


def prime_generator(bitlen):
    # 'min' and 'max' is a bitlen-bit random's range
    max = (2 ** bitlen) - 1
    min = 2 ** (bitlen - 1)
    p = 0
    # if p<=min, create a random again
    while (p <= min):
        p = secrets.randbelow(max)
    # find the nearest prime from p. if p isn't a prime, p++
    while (MR_test(p) == 0):
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
    return (n, e, d, p, q)


def encrypt(n, e, m):
    return FastExp(m, e, n)


def decrypt(p, q, d, n, c):
    Vp = FastExp(c, d % (p - 1), p)
    Vq = FastExp(c, d % (q - 1), q)
    Xp = q * Invert(q, p)
    Xq = p * Invert(p, q)
    m = (Vp * Xp + Vq * Xq) % n
    return m


if __name__ == "__main__":
    n, e, d, p, q = rsa_init()
    m = int(input("m: "))

    start = time.perf_counter()
    c = encrypt(n, e, m)
    end = time.perf_counter()
    print("encrypt: {}".format(c))
    print("encrypt took time: {}".format(end - start))

    print(">>>")
    start = time.perf_counter()
    m = decrypt(p, q, d, n, c)
    end = time.perf_counter()
    print("decrypt: {}".format(m))
    print("decrypt took time: {}".format(end - start))

    print(">>>")
    start = time.perf_counter()
    m = FastExp(c, d, n)
    end = time.perf_counter()
    print("decrypt: {}".format(m))
    print("decrypt without CRT took time: {}".format(end - start))
    os.system("pause")
