import os


def Rail_Fence(s, n):
    L = []
    for i in range(n):
        for j in range(i, len(s), n):
            L.append(s[j])
    return "".join(L)


def de_Rail_Fence(s, n):
    L2, L, length, judge = [], [], len(s) // n, len(s) % n
    if judge != 0:
        length += 1
    for i in range(n):
        if length * (i + 1) < len(s):
            L.append(s[length * i:length * (i + 1)])
        else:
            L.append(s[length * i:len(s)])
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
        n = int(input("num of lines: "))
        s = input("input text: ")
        print(de_Rail_Fence(s, n))
    os.system("pause")
