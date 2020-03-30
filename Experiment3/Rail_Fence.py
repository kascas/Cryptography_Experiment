import os


def Rail_Fence(s, n):
    L = []
    for i in range(n):
        for j in range(i, len(s), n):
            L.append(s[j])
    return "".join(L)


def de_Rail_Fence(s, n):
    L, count, pos, result = [], [len(s) // n] * n, 0, []
    for i in range(len(s) % n):
        count[i] += 1
    for i in range(n):
        L.append(s[pos:pos + count[i]])
        pos += count[i]
    print(L)
    if len(s) % n != 0:
        length = len(s) // n + 1
    else:
        length = len(s) // n
    for i in range(length):
        for j in range(n):
            if i <= count[j] - 1:
                result.append(L[j][i])
            else:
                continue
    return "".join(result)


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
