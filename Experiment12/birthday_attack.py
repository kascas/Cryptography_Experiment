import os
import random
import math
from SHA1 import *

SHA1_MAX = 2 ** 64


def test(a, b, n):
    # test high n bits of a and b
    if ((a ^ b) >> (160 - n)) == 0:
        return 1
    else:
        return 0


def messageGen():
    # a random value of message
    mValue = random.randrange(1, SHA1_MAX)
    # turn mValue into message(bytes)
    m = mValue.to_bytes(math.ceil(len(hex(mValue).replace('0x', '')) / 2), 'big')
    return m


def attack(hStr, n):
    hValue = int(hStr, 16)
    while (True):
        # create a random message
        mTest = messageGen()
        H = SHA1()
        # compute hash of the message
        H.hash(mTest)
        mValue = int(H.hexdigest(), 16)
        # test
        if test(hValue, mValue, n):
            return mTest


if __name__ == "__main__":
    hStr = 'a9993e364706816aba3e25717850c26c9cd0d89d'
    n = int(input('n: '))
    m = attack(hStr, n)
    print('probably message: {}'.format(m))
    print('>>>Test')
    H = SHA1()
    H.hash(m)
    print('  given hash: {}'.format(hStr))
    print('message hash: {}'.format(H.hexdigest()))
    os.system('pause')
