from Numtheory import *
from ECC_compute import *
import hashlib


def KeyGen(GLOBAL):
    p, E, G, n = GLOBAL
    d = random.randrange(1, n)
    Q = multi(G, d, GLOBAL)
    return (Q, d)


def sign(M, GLOBAL, d):
    p, E, G, n = GLOBAL
    r, s = 0, 0
    while (True):
        k = random.randrange(1, n)
        point = multi(G, k, GLOBAL)
        r = point[0] % n
        # if r==0, back to the beginning
        if r == 0:
            continue
        t = Invert(k, n)
        # e = hash(M)
        ep = hashlib.sha256(M).digest()
        e = OS2IP(ep)
        s = (t * (e + d * r)) % n
        if s == 0:
            continue
        else:
            break
    return (r, s)


def verify(M, GLOBAL, Q, S):
    p, E, G, n = GLOBAL
    r, s = S
    # if r>=n or s>=n, verify fails
    if r >= n or s >= n:
        return -1
    ep = hashlib.sha256(M).digest()
    e = OS2IP(ep)
    # w=s^-1 mod n
    w = Invert(s, n)
    u1, u2 = e * w, r * w
    # X = u1*G + u2*Q
    X = plus(multi(G, u1, GLOBAL), multi(Q, u2, GLOBAL), GLOBAL)
    # if X == O
    if X == (-1, -1):
        return -1
    v = X[0] % n
    if v == r:
        return 1
    else:
        return -1


if __name__ == "__main__":
    p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
    Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
    n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    E = (a, b)
    GLOBAL = (p, E, (Gx, Gy), n)

    Q, d = KeyGen(GLOBAL)
    m = input('m: ')
    M = m.encode('utf-8')
    S = sign(M, GLOBAL, d)
    result = verify(M, GLOBAL, Q, S)

    print('sign: {}'.format(S))
    print('verify: {}'.format(result))
