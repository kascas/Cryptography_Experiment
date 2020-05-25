from ECC_compute import *
from Numtheory import *

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
    return (p, E, G)
'''


def KeyGenerator(GLOBAL):
    p, E, G, n = GLOBAL
    N = random.randrange(1, n)
    P = multi(G, N, GLOBAL)
    return (P, N)


def secret(GLOBAL, N, P):
    return multi(P, N, GLOBAL)


if __name__ == "__main__":
    p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
    Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
    n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    E = (a, b)
    GLOBAL = (p, E, (Gx, Gy), n)

    (Pa, Na) = aKey = KeyGenerator(GLOBAL)
    (Pb, Nb) = bKey = KeyGenerator(GLOBAL)
    secretA = secret(GLOBAL, Na, Pb)
    secretB = secret(GLOBAL, Nb, Pa)

    print('A\'s key: {}'.format(secretA))
    print('B\'s key: {}'.format(secretB))
