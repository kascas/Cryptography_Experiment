from SHA1 import *


class HMAC:
    def __init__(self, k, hashstr):
        self.k = k
        self.b, self.n = 0, 0
        if hashstr == 'sha1':
            self.b = 512
            self.n = 160

    def kjudge(self):
        kvalue = int.from_bytes(self.k, 'big')
        # if len(k) > b
        if kvalue >> 512 != 0:
            h = SHA1()
            h.hash(self.k)
            # k = hash(k)
            self.k = int(h.hexdigest(), 16).to_bytes(self.b // 8, 'big')
        return

    def kplus(self):
        return self.k.rjust(self.b // 8, b'\x00')

    def mac(self, m):
        self.kjudge()
        ipad = b'\x36' * (self.b // 8)
        opad = b'\x5c' * (self.b // 8)
        # s1 = k+ ^ ipad
        s1 = (int.from_bytes(self.kplus(), 'big') ^
              int.from_bytes(ipad, 'big')).to_bytes(self.b // 8, 'big')
        hashIn1 = s1 + m
        h1 = SHA1()
        h1.hash(hashIn1)
        # hashOut1 = hash(s1||m)
        hashOut1 = int(h1.hexdigest(), 16).to_bytes(self.b // 8, 'big')
        # s2 = k+ ^ opad
        s2 = (int.from_bytes(self.kplus(), 'big') ^
              int.from_bytes(opad, 'big')).to_bytes(self.b // 8, 'big')
        hashIn2 = s2 + hashOut1
        h2 = SHA1()
        h2.hash(hashIn2)
        # return hash(s2||hashOut1)
        return h2.hexdigest()


if __name__ == "__main__":
    h = HMAC(k=(input('key: ')).encode('utf-8'), hashstr='sha1')
    print('MAC: {}'.format(h.mac(m=input('message: ').encode('utf-8'))))
