from Numtheory import *
from ECC_compute import *
import os

'''
def init():
    a, b, p = 0, 0, 0
    while (True):
        # 160-bit prime p
        p = prime(160)
        # curve's parameter a, b
        a, b = random.randrange(1, p), random.randrange(1, p)
        # 'p%8 != 1' is to make finding root mod p easy
        if (4 * (a ** 3) + 27 * (b ** 2)) % p != 0 and p % 8 != 1:
            break
    E, G = (a, b), (0, 0)
    while (True):
        # random G's x-coordinate
        Gx = random.randrange(1, p)
        # tmp = Gx^3 + a*Gx + b
        tmp = (Gx ** 3) + a * Gx + b
        # if y exists (y^2)=Gx^3+a*Gx+b mod p
        if jacobi(tmp, p) == 1:
            # get G's coordinate
            Gy = root_mod(Gx, p)[0]
            if Gy != 0:
                G = (Gx, Gy)
                break
    Na = random.randrange(1, p)
    Pa = multi(G, Na, p, E)
    return ((p, E, G), Na, Pa)
'''


def KeyGenerator(GLOBAL):
    p, E, G, n = GLOBAL
    N = random.randrange(1, n)
    P = multi(G, N, GLOBAL)
    return (N, P)


def encrypt(GLOBAL, Pa, M):
    p, E, G, n = GLOBAL
    k = random.randrange(1, n)
    C1 = multi(G, k, GLOBAL)
    C2 = plus(M, multi(Pa, k, GLOBAL), GLOBAL)
    return (C1, C2)


def decrypt(GLOBAL, Na, C):
    C1, C2 = C
    tmp = negative(multi(C1, Na, GLOBAL), GLOBAL)
    M = plus(C2, tmp, GLOBAL)
    return M


if __name__ == "__main__":
    p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
    Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
    n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    E = (a, b)
    GLOBAL = (p, E, (Gx, Gy), n)

    private, public = KeyGenerator(GLOBAL)
    M = pointGenerator(GLOBAL)
    C1, C2 = encrypt(GLOBAL, public, M)
    Mp = decrypt(GLOBAL, private, (C1, C2))

    print('M: {}\n'.format(M))
    print('public  key: {}\n'.format(public))
    print('private key: {}\n'.format(private))
    print('encrypt: {}\n'.format((C1, C2)))
    print('decrypt: {}\n'.format(M))

    os.system('pause')
