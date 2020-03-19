import os
from GCD import GCD


def Affine_Cipher(s, a, b, n):
    L = []
    for i in range(len(s)):
        #turn characters into asc, then crypt
        L.append(chr(((ord(s[i]) - ord('a')) * a + b) % n + ord('a')))
    return "".join(L)


def de_Affine_Cipher(s, a, b, n):
    L = []
    m = GCD(a, n)[1]
    for i in range(len(s)):
        #turn characters into asc, then decrypt
        L.append(chr(((ord(s[i]) - ord('a') - b) * m) % n + ord('a')))
    return "".join(L)


if __name__=="__name__":
    judge = int(input("please choose [1]crypt, [2]decrypt:  "))
    if (judge == 1):
        c = str(input("input c: "))
        a = int(input("a= "))
        b = int(input("b= "))
        n = int(input("how many characters in this language: "))
        print(Affine_Cipher(c, a, b, n))
    else:
        c = str(input("input c: "))
        a = int(input("a= "))
        b = int(input("b= "))
        n = int(input("how many characters in this language: "))
        print(de_Affine_Cipher(c, a, b, n))
    os.system("pause")
