import math
import hashlib


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
        mask = fp.readline()
        if len(key) < 16:
            key += b'\x00' * (16 - len(key))
        else:
            key = key[0:16]
        if len(mask) < 16:
            mask += b'\x00' * (16 - len(mask))
        else:
            mask = mask[0:16]
    return key, mask


def padding(buf):
    bufList, padLen = [], len(buf) % 16
    listLen = math.ceil(len(buf) / 16)
    for i in range(listLen):
        pad = hashlib.sha1(buf).hexdigest().replace('0x', '')[0:(16 - padLen)].encode('utf-8')
        bufList.append(buf[-1 * padLen:] + pad)
    return bufList
