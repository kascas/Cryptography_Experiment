import os
import random
from Numtheory import *


def rabin_init():
    p = prime(512)
    q = prime(512)
    n = p * q
    return ((p, q), n)


def r(m):
    return m


def r_Invert(m):
    return m


def sign(m, pr):
    p, q = pr
    M = function_r(m)
    s1_1, s1_2 = srm_prime(M, p)
    s2_1, s2_2 = srm_prime(M, q)
    s = [CRT([s1_1, s2_1], [p, q], 2),
         CRT([s1_2, s2_1], [p, q], 2),
         CRT([s1_1, s2_2], [p, q], 2),
         CRT([s1_2, s2_2], [p, q], 2)]
    sel = random.randint(1, 100) % 4 + 1
    return s[sel]


def verify(m, s, pu):
    n = pu
    M = s * s % n


if __name__ == "__main__":
    # s = sign(23, (7, 11))
    # verify(23, s, 77)
    print(srm_prime(25, 77))
