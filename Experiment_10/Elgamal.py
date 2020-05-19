import os
import random
import hashlib
from Numtheory import *


def OS2IP(x_array):
    xLen, x, base = len(x_array), 0, 1
    for i in range(xLen):
        x = x + x_array[xLen - 1 - i] * base
        base = base * 256
    return x


def init(k=128):
    '''
    find safe prime's primitive root
        is much easier than general prime's
    safe prime: p=2*q+1 (both p and q are primes)
    find safe prime's primitive root:
        (g^2 mod p !=1) and (g^q mod q !=1)
    :param k: the bit length of p
    :return: pu(public key) and pr(private key)
    '''
    # find safe prime p
    while (1):
        p = prime(k)
        q = (p - 1) >> 1
        if MR_test(q) == 1:
            break
    # find p's primitive root
    while (1):
        g = random.randrange(2, p)
        if FastExp(g, 2, p) != 1 and FastExp(g, q, p) != 1:
            break
    # random x
    x = random.randrange(1, p - 1)
    y = FastExp(g, x, p)
    pu = (p, g, y)
    pr = (p, g, x)
    return (pu, pr)


def sign(M, pr):
    # M's hash value
    mHash = OS2IP(hashlib.sha1(M).digest())
    p, g, x = pr
    k = p - 1
    # select k which is coprime to p-1
    while GCD(k, p - 1)[0] != 1:
        k = random.randint(1, p - 1)
    s1 = FastExp(g, k, p)
    s2 = (mHash - x * s1) * Invert(k, p - 1) % (p - 1)
    return (s1, s2)


def verify(S, M, pu):
    p, g, y = pu
    s1, s2 = S
    mHash = OS2IP(hashlib.sha1(M).digest())
    v1 = FastExp(g, mHash, p)
    v2 = FastExp(y, s1, p) * FastExp(s1, s2, p) % p
    if v1 == v2:
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
    print('verify: {}'.format(verify(S, M, pu)))
    os.system("pause")
