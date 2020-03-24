import os


def Rail_Fence(s, n):
    L = []
    for i in range(n):
        for j in range(i, len(s), n):
            L.append(s[j])
    return "".join(L)


def de_Rail_Fence(L, n):
    L2 = []
    for i in range(len(L[0])):
        for j in range(n):
            if (i > len(L[j]) - 1):
                continue
            L2.append(L[j][i])
    return "".join(L2)


if __name__ == "__main__":
    judge = int(input("please choose [1]crypt, [2]decrypt: "))
    if (judge == 1):
        n = int(input("num of lines: "))
        s = input("input text: ")
        print(Rail_Fence(s, n))
    else:
        L = []
        n = int(input("num of lines: "))
        for i in range(n):
            L.append(input())
        print(de_Rail_Fence(L, n))
    os.system("pause")
