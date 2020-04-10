from Crypto.Cipher import AES
import time
import os


def NkJudge(key):
    Nk = 0
    if len(hex(key).replace("0x", "")) <= 32:
        Nk = 4
    elif len(hex(key).replace("0x", "")) <= 48:
        Nk = 6
    elif len(hex(key).replace("0x", "")) <= 64:
        Nk = 8
    else:
        print("keylen > 256")
        return 0
    return Nk


if __name__ == "__main__":
    mode = int(input("mode: "))
    message = int(input("text: "), 16).to_bytes(16, 'big')
    k = int(input("key: "), 16)
    Nk = NkJudge(k)
    key = k.to_bytes(Nk * 4, 'big')
    obj = AES.new(key, AES.MODE_ECB)
    start, end = 0, 0
    if mode == 1:
        start = time.perf_counter()
        for i in range(1000):
            c = obj.encrypt(message)
        end = time.perf_counter()
    else:
        start = time.perf_counter()
        for i in range(1000):
            c = obj.decrypt(message)
        end = time.perf_counter()
    print("\n>>>result: " + hex(int.from_bytes(c, 'big')))
    print("AES took time: {} s".format((end - start)))
    os.system("pause")
