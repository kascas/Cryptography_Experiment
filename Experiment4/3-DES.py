import os
from DES import *


def DES_3(p, key, mode):
    if mode == 1:
        key1, key2 = key >> 64, key & int("0xffffffffffffffff", 16)
        c1 = int(DES(p, key1, 1), 16)
        c2 = int(DES(c1, key2, 2), 16)
        result = int(DES(c2, key1, 1), 16)
    else:
        key1, key2 = key >> 64, key & int("0xffffffffffffffff", 16)
        p1 = int(DES(p, key1, 2), 16)
        p2 = int(DES(p1, key2, 1), 16)
        result = int(DES(p2, key1, 2), 16)
    return hex(result).replace("0x", "").zfill(16)


if __name__ == "__main__":
    mode = int(input("mode: [1]crypt [2]decrypt "))
    p = int(input("input text: "), 16)
    key = int(input("input key: "), 16)
    print("\nciphertext is: " + DES_3(p, key, mode))
    os.system("pause")
