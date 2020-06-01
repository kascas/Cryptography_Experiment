import os


class SM3:
    def __init__(self):
        self.H = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600,
                  0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]

    @staticmethod
    def shift(w, n):
        # use n%32 instead of n (if n>32)
        return ((w << n % 32) | (w >> (32 - n % 32))) & 0xffffffff

    @staticmethod
    def P0(x):
        return x ^ SM3.shift(x, 9) ^ SM3.shift(x, 17)

    @staticmethod
    def P1(x):
        return x ^ SM3.shift(x, 15) ^ SM3.shift(x, 23)

    @staticmethod
    def FF(x, y, z, round):
        if round <= 15:
            return x ^ y ^ z
        else:
            return (x & y) | (x & z) | (y & z)

    @staticmethod
    def GG(x, y, z, round):
        if round <= 15:
            return x ^ y ^ z
        else:
            return (x & y) | (~x & z)

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

    @staticmethod
    def w_init(B):
        w = [0 for i in range(68)]
        wp = [0 for i in range(64)]
        for i in range(16):
            w[i] = int.from_bytes(B[i * 4:(i + 1) * 4], 'big')
        for i in range(16, 68):
            w[i] = SM3.P1(w[i - 16] ^ w[i - 9] ^ SM3.shift(w[i - 3], 15)) ^ \
                   SM3.shift(w[i - 13], 7) ^ w[i - 6]
        for i in range(64):
            wp[i] = w[i] ^ w[i + 4]
        return w, wp

    # compress 512-bit into 256-bit
    def compress(self, B):
        a, b, c, d, e, f, g, h = self.H
        MASK = 0xffffffff
        w, wp = SM3.w_init(B)

        for i in range(64):
            if i <= 15:
                t = 0x79cc4519
            else:
                t = 0x7a879d8a
            ss1 = SM3.shift((SM3.shift(a, 12) + e + SM3.shift(t, i)) & MASK, 7)
            ss2 = ss1 ^ SM3.shift(a, 12)
            tt1 = (SM3.FF(a, b, c, i) + d + ss2 + wp[i]) & MASK
            tt2 = (SM3.GG(e, f, g, i) + h + ss1 + w[i]) & MASK
            d = c
            c = SM3.shift(b, 9)
            b = a
            a = tt1
            h = g
            g = SM3.shift(f, 19)
            f = e
            e = SM3.P0(tt2)
        self.H[0] = a ^ self.H[0]
        self.H[1] = b ^ self.H[1]
        self.H[2] = c ^ self.H[2]
        self.H[3] = d ^ self.H[3]
        self.H[4] = e ^ self.H[4]
        self.H[5] = f ^ self.H[5]
        self.H[6] = g ^ self.H[6]
        self.H[7] = h ^ self.H[7]

    # compute hash
    def hash(self, m):
        mList = SM3.block(SM3.padding(m))
        for i in range(len(mList)):
            self.compress(mList[i])
        return

    # turn int into string
    def hexdigest(self):
        p = ''
        for i in range(8):
            p += hex(self.H[i])[2:].zfill(8)
        return p


if __name__ == "__main__":
    s = SM3()
    m = input('message: ').encode('utf-8')
    s.hash(m)
    print('SM3 hash: {}'.format(s.hexdigest()))
    os.system('pause')
