def GCD(a, b):
    x1, y1, x2, y2 = 1, 0, 0, 1
    t1, t2 = 0, 0
    L = []
    while (1):
        t1, t2 = x2, y2
        x2, y2 = x1 - (a // b) * x2, y1 - (a // b) * y2
        x1, y1 = t1, t2
        if (a % b) == 0:
            break
        a, b = b, a % b
    if b < 0:
        b, x1, y1 = (-1) * b, (-1) * x1, (-1) * y1
    L = [b, x1, y1]
    return L


def Era():
    n = int(input("input n= "))
    L = []
    count = 0
    for i in range(n + 1):
        L.append(1)
    for i in range(2, int(math.sqrt(n)) + 1):
        if (L[i] == 1):
            j = i * i
            while (j <= n):
                L[j] = 0
                j += i
    for i in range(2, n + 1):
        if (L[i] == 1):
            print(i, end="  ")
            count += 1
    print("\ntotal: {}".format(count))


def FastExp(x, n, m):
    d = 1
    while n > 0:
        if (n % 2) == 1:
            d = (d * x) % m
            n = (n - 1) // 2
        else:
            n = n // 2
        x = (x * x) % m
    return d
