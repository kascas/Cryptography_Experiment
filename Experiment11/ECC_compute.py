from Numtheory import *


def plus(point1, point2, GLOBAL):
    p, E, G, n = GLOBAL
    (xp, yp), (xpoint, ypoint) = point1, point2
    if point1 == negative(point2, GLOBAL):
        print('p1 + p2 = +oo')
        return (-1, -1)
    if point1 != point2:
        delta = ((ypoint - yp) * Invert((xpoint - xp), p)) % p
    else:
        delta = ((3 * xp * xp + E[0]) * Invert((2 * yp), p)) % p
    x = ((delta ** 2) - xp - xpoint) % p
    y = (delta * (xp - x) - yp) % p
    return (x, y)


def multi(point, times, GLOBAL):
    p, E, G, n = GLOBAL
    tmp, result = point[:], (-1, -1)
    while (times > 0):
        if times & 1:
            if result == (-1, -1):
                result = tmp[:]
            else:
                result = plus(result, tmp, GLOBAL)[:]
        tmp = plus(tmp, tmp, GLOBAL)[:]
        times >>= 1
    return result


def negative(point, GLOBAL):
    p, E, G, n = GLOBAL
    return (point[0], -point[1] % p)


def pointGenerator(GLOBAL):
    p, E, G, n = GLOBAL
    (a, b), M = E, (0, 0)
    while (True):
        # random M's x-coordinate
        Mx = random.randrange(1, p)
        # tmp = Mx^3 + a*Mx + b
        tmp = (Mx ** 3) + a * Mx + b
        # if y exists (y^2)=Gx^3+a*Gx+b mod p
        if jacobi(tmp, p) == 1:
            # get G's coordinate
            My = root_mod(Mx, p)[0]
            if My != 0:
                M = (Mx, My)
                break
    return M
