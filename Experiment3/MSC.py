import os


def MSC(s, c):
    result = []
    for i in range(len(c)):
        result.append(s[ord(c[i]) - ord('a')])
    return "".join(result)


def de_MSC(s, c):
    result = []
    for i in range(len(c)):
        for j in range(len(s)):
            if (c[i] == s[j]):
                result.append(chr(j + ord('a')))
    return "".join(result)


if __name__ == "__main__":
    judge = int(input("please choose [1]crypt,[2]decrypt: "))
    if (judge == 1):
        s = str(input("input list: "))
        c = str(input("input text: "))
        print("result is: " + MSC(s, c))
    else:
        s = str(input("input list: "))
        c = str(input("input ciphertext: "))
        print("result is: " + de_MSC(s, c))
    os.system("pause")
