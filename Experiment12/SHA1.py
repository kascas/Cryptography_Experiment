import os
import hashlib


class SHA1:

    def __init__(self):
        self.H = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]

    # pad the message
    @staticmethod
    def padding(m):
        tmp, mLen = 0, len(m)
        if mLen % 64 != 56:
            tmp = (56 - mLen) % 64 - 1
            m = m + b'\x80' + tmp * b'\x00'
        m += (mLen * 8).to_bytes(8, 'big')
        return m

    # divide message into 512-bit blocks
    @staticmethod
    def block(m):
        mList = []
        for i in range(len(m) // 64):
            mList.append(m[i * 64:(i + 1) * 64])
        return mList

    # left shift
    @staticmethod
    def shift(w, n):
        return ((w << n) | (w >> (32 - n))) & 0xffffffff

    # compute w[80]
    @staticmethod
    def w_init(Y):
        w = [0 for i in range(80)]
        for i in range(16):
            w[i] = int.from_bytes(Y[i * 4:(i + 1) * 4], 'big')
        for i in range(16, 80):
            w[i] = SHA1.shift(w[i - 16] ^ w[i - 14] ^ w[i - 8] ^ w[i - 3], 1)
        return w

    # compress 512-bit into 160-bit
    def compress(self, Y):
        w = SHA1.w_init(Y)
        a, b, c, d, e = self.H
        # 80 rounds
        for i in range(80):
            if i <= 19:
                k = 0x5a827999
                f = (b & c) ^ ((~b) & d)
            elif i <= 39:
                k = 0x6ed9eba1
                f = b ^ c ^ d
            elif i <= 59:
                k = 0x8f1bbcdc
                f = (b & c) ^ (b & d) ^ (c & d)
            else:
                k = 0xca62c1d6
                f = b ^ c ^ d
            t = (SHA1.shift(a, 5) + f + e + w[i] + k) & 0xffffffff
            e = d
            d = c
            c = SHA1.shift(b, 30)
            b = a
            a = t
        self.H[0] = (a + self.H[0]) & 0xffffffff
        self.H[1] = (b + self.H[1]) & 0xffffffff
        self.H[2] = (c + self.H[2]) & 0xffffffff
        self.H[3] = (d + self.H[3]) & 0xffffffff
        self.H[4] = (e + self.H[4]) & 0xffffffff

    # compute hash
    def hash(self, m):
        mList = SHA1.block(SHA1.padding(m))
        for i in range(len(mList)):
            self.compress(mList[i])
        return

    # turn int into string
    def hexdigest(self):
        p = ''
        for i in range(5):
            p += hex(self.H[i])[2:].zfill(8)
        return p


if __name__ == "__main__":
    m = str(input('message: '))
    m_encode = m.encode('utf-8')

    h = SHA1()
    h.hash(m_encode)

    print('   mine: {}'.format(h.hexdigest()))
    print('hashlib: {}'.format(hashlib.sha1(m_encode).hexdigest()))
