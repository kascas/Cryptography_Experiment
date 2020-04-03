import os
from SDES import *


def KeyCrypt(p):
    List = []
    for key in range(1024):
        List.append(SDES(p, key, 1))
    return List


def KeyDecrypt(p, c):
    List, result = KeyCrypt(p), []
    for key2 in range(1024):
        z = SDES(c, key2, 2)
        for key1 in range(1024):
            if z == List[key1]:
                result.append((key1, key2))
    print(result)
    return result


def KeyTest(p, c, List):
    result, judge = [], 0
    for i in range(len(List)):
        judge = 0
        if SDES(p, List[i][0], 1) != SDES(c, List[i][1], 2):
            judge += 1
        if judge == 0:
            result.append(List[i])
    return result


if __name__ == "__main__":
    x = int(input("x: "), 16)
    y = int(input("y: "), 16)
    List = KeyDecrypt(x, y)
    while (1):
        p = int(input("another p: "), 16)
        c = int(input("another c: "), 16)
        List = KeyTest(p, c, List)
        print(List)
        if (len(List) == 1):
            break
    print("\n>>>key1: " + hex(List[0][0]))
    print(">>>key2: " + hex(List[0][1]))
    # print("key1: " + hex(KeyTest(p, c, List)[0]))
    # print("key2: " + hex(KeyTest(p, c, List)[1]))
    os.system("pause")
