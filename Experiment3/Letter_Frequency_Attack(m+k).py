import os


def LFA(c):
    L, judge, select, max = [0] * 26, ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f',
                                       'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z'], 0, 0
    for i in range(len(c)):
        if c[i] != ' ':
            L[ord(c[i]) - ord("a")] += 1
    for i in range(26):
        if L[i] > max:
            max, select = L[i], i
    print(L)
    for i in range(len(judge)):
        move = (select - (ord(judge[i]) - ord("a")) + 26) % 26
        print("k= {:2}  plaintext is: ".format(move), end="")
        for j in range(len(c)):
            if (c[j] != ' '):
                print(chr((ord(c[j]) + 26 - move) % 26 + ord("a")), end="")
        print()


if __name__ == "__main__":
    c = input("input c:").lower()
    LFA(c)
    os.system("pause")
