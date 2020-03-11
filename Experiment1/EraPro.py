import sys


def EraPro(n):
    list = [1] * ((n >> 6) + 1)
    for i in range(3, n + 1, 2):
        if not ((list[i >> 6] >> ((i >> 1) % 32)) & 1):
            print(i)
            for j in range(i * i, n + 1, i):
                if j % 2 == 1:
                    list[j >> 6] |= (1 << ((j >> 1) % 32))
    return list

print(sys.getsizeof(2**40))
n=int(input("n= "))
EraPro(n)

