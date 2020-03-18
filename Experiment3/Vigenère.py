import os


def Vigenere(c, key):
    key_L, result_L = [], []
    for i in range(len(key)):
        key_L.append(ord(key[i]) - ord("a"))
    for i in range(len(c)):
        result_L.append(chr((ord(c[i]) - ord("a") + key_L[i % len(key)]) % 26 + ord("a")))
    return "".join(result_L)


if __name__ == "__main__":
    c = input("input plaintext: ")
    key = input("input key: ")
    print("result is: " + Vigenere(c, key))
