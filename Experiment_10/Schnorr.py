import os
import random
import secrets
import hashlib
from Numtheory import *


def init():
    # prime numbers 'p' and 'q'
    # 'q' is selected
    # 'p' is needed to be compute according to 'q'
    p = prime(1024)
    q = prime(160)
    n = p // q
    # 'n' is quotient of p/q
    # 'n++' and 'MR_test' can find 'p'
    while (1):
        p = q * n + 1
        if (MR_test(p) == 1):
            break
        n += 1
    # a**q = 1 mod q
    # as for every 'tmp', tmp**(n*q) = 1 mod p
    # replace 'a' with 'tmp**n' to accelerate
    tmp = 2
    while (1):
        a = FastExp(tmp, n, p)
        if a > 1:
            break
        tmp += 1
    s = random.randint(1, q)
    v = Invert(FastExp(a, s, p), p)
    pu = (p, q, a, v)
    pr = (p, q, a, s)
    return (pu, pr)


def sign(M, pr):
    p, q, a, s = pr
    r = random.randint(1, q - 1)
    x = FastExp(a, r, p)
    # OS2IP turns bytearray into biginteger
    # I2OSP turns biginteger into bytearray
    e = OS2IP(hashlib.sha1(M + I2OSP(x, bytelen(x))).digest())
    y = (r + s * e) % q
    return (e, y)


def verify(M, S, pu):
    p, q, a, v = pu
    e, y = S
    xp = FastExp(a, y, p) * FastExp(v, e, p) % p
    # OS2IP turns bytearray into biginteger
    # I2OSP turns biginteger into bytearray
    ep = OS2IP(hashlib.sha1(M + I2OSP(xp, bytelen(xp))).digest())
    if ep == e:
        return 1
    else:
        return -1


if __name__ == "__main__":
    pu, pr = init()
    print('public  key: {}'.format(pu))
    print('private key: {}'.format(pr))
    m = input("m: ")
    M = m.encode('utf-8')
    S = sign(M, pr)
    print('verify: {}'.format(verify(M, S, pu)))
    os.system("pause")
