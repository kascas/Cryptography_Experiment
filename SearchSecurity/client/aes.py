import math


def getFileKey():
    with open('./FILE.KEY', 'rb') as fp:
        key = fp.readline()
        iv = fp.readline()
        if len(key) < 16:
            key += b'\x00' * (16 - len(key))
        else:
            key = key[0:16]
        if len(iv) < 16:
            iv += b'\x00' * (16 - len(iv))
        else:
            iv = iv[0:16]
    return key, iv


def getWordKey():
    with open('./WORD.KEY', 'rb') as fp:
        key = fp.readline()
        if len(key) < 16:
            key += b'\x00' * (16 - len(key))
        else:
            key = key[0:16]
    return key


def padding(buf):
    bufList, length = [], len(buf)
    listLen = math.ceil(length / 16)
    for i in range(listLen - 1):
        bufList.append(buf[i * 16:(i + 1) * 16])
    bufPad = buf[-1 * (length % 16):] + (16 - length % 16) * b'\x00'
    bufList.append(bufPad)
    return bufList
