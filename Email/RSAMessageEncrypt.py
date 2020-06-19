import secrets
from RSA_OAEP import *
from Numtheory import *
import math


def _rsa_init(email):
    eStr = email.encode('utf-8')
    e = OS2IP(eStr)
    while True:
        p = _prime_generator(512)
        q = _prime_generator(512)
        n, phi = p * q, (p - 1) * (q - 1)
        if GCD(e, phi)[0] == 1:
            break
    d = Invert(e, phi)
    with open('./PUBLIC.KEY', 'w') as fp1, open('./PRIVATE.KEY', 'w') as fp2:
        fp1.write(hex(n) + '\n')
        fp1.write(hex(e))
        fp2.write(hex(n) + '\n')
        fp2.write(hex(d))
    return


def _prime_generator(bitlen):
    # 'min' and 'max' is a bitlen-bit random's range
    max = (2 ** bitlen) - 1
    min = 2 ** (bitlen - 1)
    p = random.randrange(min, max)
    # find the nearest prime from p. if p isn't a prime, p++
    while (MR_test(p) == 0):
        p = random.randrange(min, max)
    return p


def _RSA_encrypt(private, m):
    n, e = private
    c = b''
    blockNum = math.ceil(len(m) / 64)
    for i in range(blockNum):
        c += RSAES_OAEP_E(n, e, m[i * 64:(i + 1) * 64])
    return c


def _RSA_decrypt(public, c):
    n, d = public
    m = b''
    blockNum = len(c) // 128
    for i in range(blockNum):
        m += RSAES_OAEP_D(n, d, c[i * 128:(i + 1) * 128])
    return m


if __name__ == "__main__":
    _rsa_init('liangxp2360@163.com')
    with open('./PUBLIC.KEY', 'r') as fp1, open('./PRIVATE.KEY', 'r') as fp2:
        private = fp1.readlines()
        n = int(private[0], 16)
        e = int(private[1], 16)
        d = int(fp2.readlines()[1], 16)
    M = 'fuihumhwumwcgwgxeeiwxwheigxhwiegcmwegigcxhiwemghxwieguxierumgesihrughierhgierhgihgdshghcrhgiurcghximagcimhxawimgchawimgiacuegmaiegmciauwhmigawegicawiegw'.encode(
        'utf-8')
    c = _RSA_encrypt((n, e), M)[0:-1] + b'\x05'
    print(c)
    print(_RSA_decrypt((n, d), c).decode('utf-8'))
