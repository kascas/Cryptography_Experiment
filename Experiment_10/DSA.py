from Numtheory import *
import random
import hashlib
import os


def init():
    # prime numbers 'p' and 'q'
    # 'q' is selected
    # 'p' is needed to be compute according to 'q'
    pLen = random.randrange(512, 1025, 64)
    while (1):
        p = prime(pLen)
        q = prime(160)
        n = p // q
        # 'n' is quotient of p/q
        # 'n++' and 'MR_test' can find 'p'
        while (1):
            p = q * n + 1
            if (MR_test(p) == 1):
                break
            n += 1
        if bitlen(p) % 64 == 0:
            break
    tmp, g = 2, 0
    # compute g=h^((p-1)/q) mod p
    while (1):
        g = FastExp(tmp, n, p)
        if g > 1:
            break
        tmp += 1
    x = random.randint(1, q)
    y = FastExp(g, x, p)
    return ((p, q, g, y), (p, q, g, x))


def sign(M, pr):
    p, q, g, x = pr
    k = random.randint(0, q)
    # r=(g^k mod p) mod q
    r = FastExp(g, k, p) % q
    # H=sha1(M)
    H = OS2IP(hashlib.sha1(M).digest())
    # s=k^(-1)*(H+x*r) mod q
    s = Invert(k, q) * (H + x * r) % q
    # turn 'r' and 'q' into bytearray
    r_byte = I2OSP(r, bytelen(r))
    s_byte = I2OSP(s, bytelen(s))
    return (M, r_byte, s_byte)


def verify(M, r_byte, s_byte, pu):
    p, q, g, y = pu
    # turn r_byte and s_byte into BigInteger
    r, s = OS2IP(r_byte), OS2IP(s_byte)
    # H=sha1(M)
    H = OS2IP(hashlib.sha1(M).digest())
    # w=s^(-1) mod q
    w = Invert(s, q)
    # u1=H*w mod q, u2=r*w mod q
    u1, u2 = H * w % q, r * w % q
    # v=((g^u1)*(y^u2) mod p) mod q
    v = (FastExp(g, u1, p) * FastExp(y, u2, p) % p) % q
    if r == v:
        return 1
    else:
        return -1


if __name__ == "__main__":
    pu, pr = init()
    print("public  key: {}".format(pu))
    print("private key：{}".format(pr))
    m = input("m: ")
    M = m.encode('utf-8')
    M, r_byte, s_byte = sign(M, pr)
    print('verify: {}'.format(verify(M, r_byte, s_byte, pu)))
    os.system("pause")
