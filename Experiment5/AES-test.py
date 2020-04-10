from Crypto.Cipher import AES
import time
import os

if __name__ == "__main__":
    mode = int(input("mode: "))
    length = int(input("keylen: "))
    message = int(input("text: "), 16).to_bytes(16, 'big')
    key = int(input("key: "), 16).to_bytes(length // 8, 'big')
    obj = AES.new(key, AES.MODE_ECB)
    start, end = 0, 0
    if mode == 1:
        start = time.clock()
        c = obj.encrypt(message)
        end = time.clock()
    else:
        start = time.clock()
        c = obj.decrypt(message)
        end = time.clock()
    print(hex(int.from_bytes(c, 'big')))
    print("AES took time: {} s".format((end - start)))
    os.system("pause")
