from Crypto.Cipher import AES
import time
import os

if __name__ == "__main__":
    mode = int(input("mode: "))
    length = int(input("keylen: "))
    message = int(input("text: "), 16).to_bytes(16, 'big')
    key = int(input("key: "), 16).to_bytes(length // 8, 'big')
    start = time.clock()
    obj = AES.new(key, AES.MODE_ECB)
    end = time.clock()
    if mode == 1:
        c = obj.encrypt(message)
    else:
        c = obj.decrypt(message)
    print(hex(int.from_bytes(c, 'big')))
    print("AES took time: {} s".format((end - start)))
    os.system("pause")
