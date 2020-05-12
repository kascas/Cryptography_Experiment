def CRT(b, m, n):
    # initialize variables
    mm, bm, bmp, result = 1, 0, 0, 0
    # compute mm=m1*m2*...*mn
    for i in range(n):
        mm *= m[i]
    # compute bm=mm/mi, bmp*bm mod mi=1
    for i in range(n):
        bm = mm // m[i]
        bmp = GCD(bm, m[i])[1]
        result = (result + bm * bmp * b[i]) % mm
    # if result is negative, make it positive
    while result <= 0:
        result += mm
    return result


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


def root(n, e):
    low = 1
    height = n
    while low < height:
        mid = (low + height) // 2
        if mid ** e < n:
            low = mid + 1
        elif mid ** e > n:
            height = mid - 1
        else:
            return mid
    return -1
