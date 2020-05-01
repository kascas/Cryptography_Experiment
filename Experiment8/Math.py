import random


def FastExp(x, n, m):
    d = 1
    # if n%2==1,compute (d*x)%m,else only do (x*x)%m
    while n > 0:
        if n & 1:
            d = (d * x) % m
        n >>= 1
        x = (x * x) % m
    return d


def GCD_core(a, b):
    if (b == 0):
        return (a, 1, 0)
    else:
        g, x1, y1 = GCD_core(b, a % b)
        x0, y0 = y1, x1 - a // b * y1
        return (g, x0, y0)


def GCD(a, b):
    g, x, y = GCD_core(a, b)
    if g < 0:
        g, x, y = g * -1, x * -1, y * -1
    return (g, x, y)


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
    if result <= 0:
        result = ((result * (-1)) // mm + 1) * mm + result
    return result


def MR_test(p):
    # p_1 is p-1, initialize variables
    q = p - 1
    k, isprime = 0, 0
    # compute k,q s.t. p-1=q*(2^k)
    while q & 1 == 0:
        q >>= 1
        k += 1
    # compute r^q mod p
    for i in range(10):
        isprime = 0
        r = random.randint(2, p - 1)
        r_q = FastExp(r, q, p)
        if (r_q == 1):
            isprime += 1
        else:
            for j in range(k):
                r_q = FastExp(r, (1 << j) * q, p)
                if (r_q == p - 1):
                    isprime += 1
            if isprime == 0:
                return 0
    return 1


if __name__ == "__main__":
    count = 0
    for i in range(3, 400):
        if (MR_test(i) == 1):
            count += 1
            print(i, end=" ")
    print()
    print(count)
