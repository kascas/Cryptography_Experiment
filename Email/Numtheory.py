import random
import secrets


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


def MR_test(p):
    q, k = p - 1, 0
    # compute k,q s.t. p-1=q*(2^k)
    while q & 1 == 0:
        q >>= 1
        k += 1
    # compute r^q mod p
    for i in range(10):
        j = 0
        r = random.randint(2, p - 1)
        r_q = FastExp(r, q, p)
        if (r_q == 1) or (r_q == p - 1):
            continue
        while j < k:
            if r_q == p - 1:
                break
            r_q = FastExp(r_q, 2, p)
            j += 1
        if j == k and r_q != p - 1:
            return 0
    return 1


def prime(bitlen):
    # 'min' and 'max' is a bitlen-bit random's range
    max = (2 ** bitlen) - 1
    min = 2 ** (bitlen - 1)
    p = max + 1
    while (p >= max):
        p = 0
        # if p<=min, create a random again
        while (p <= min):
            p = secrets.randbelow(max)
        # find the nearest prime from p. if p isn't a prime, p++
        while (MR_test(p) == 0):
            p += 1
    return p


def I2OSP(x, xLen):
    if x >= 256 ** xLen:
        print("I2OSP overflow")
        return -1
    base = 256 ** (xLen - 1)
    x_array = bytearray(xLen)
    for i in range(xLen):
        x_array[i] = x // base
        x = x % base
        base = base // 256
    return x_array


def OS2IP(x_array):
    xLen, x, base = len(x_array), 0, 1
    for i in range(xLen):
        x = x + x_array[xLen - 1 - i] * base
        base = base * 256
    return x


def bytelen(x):
    length = 0
    while (x != 0):
        x >>= 8
        length += 1
    return length


def bitlen(x):
    length = 0
    while (x != 0):
        x >>= 1
        length += 1
    return length


def GF_plus(a, b):
    return a ^ b


def GF_minus(a, b):
    return a ^ b


def GF_multi(a, b, n=int("0b100011011", 2)):
    result = 0
    while (b != 0):
        if (b & 1) == 1:
            result = result ^ a
        # a = f(x) * (x ^ k)
        a = a << 1
        # it's known that "x^n mod p(x)=p(x)-x^n"
        # if a7==1, then mod n to make deg(f(x)*(x^k))<8
        if (a >> 8) & 1 == 1:
            a = a ^ n
        # do right-move to b
        b = b >> 1
        # print(bin(a).replace("0b","").zfill(8))
    return result


def GF_div(a, b):
    quo, re = 0, 0
    while (len(bin(a)) >= len(bin(b))) and a != 0:
        move = len(bin(a)) - len(bin(b))
        a = a ^ (b << move)
        quo += (1 << move)
    return (quo, a)


def jacobi(a, n):
    if a == 0:
        return 0
    if a == 1:
        return 1
    e, s = 0, 0
    while (a & 1 == 0):
        a >>= 1
        e += 1
    if e & 1 == 0:
        s = 1
    elif n % 8 == 1 or n % 8 == 7:
        s = 1
    elif n % 8 == 3 or n % 8 == 5:
        s = -1
    if n % 4 == 3 and a % 4 == 3:
        s *= -1
    n1 = n % a
    if a == 1:
        return s
    else:
        return s * jacobi(n1, a)


def srm_prime(a, p):
    ja_a_p = jacobi(a, p)
    if ja_a_p == -1:
        return -1
    b = 0
    while (1):
        b = random.randint(1, p)
        if jacobi(b, p) == -1:
            break
    s, t = 0, p - 1
    while (1):
        if t & 1 == 1:
            break
        t >>= 1
        s += 1
    a_I = Invert(a, p)
    c = FastExp(b, t, p)
    r = FastExp(a, (t + 1) // 2, p)
    for i in range(s - 1):
        d = FastExp(r * r * a_I, 2 ** (s - i - 1), p)
        if d % p == p - 1:
            r = r * c % p
        c = c * c % p
    return (r, -r)
