from Crypto.Cipher import AES
import os.path as path


def _file_encrypt(src, dest, key, iv):
    key += b'\x00' * (16 - len(key))
    iv += b'\x00' * (16 - len(iv))
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # dest = path.splitext(src)[0] + '(e)' + path.splitext(src)[1]
    with open(src, 'rb') as fr, open(dest, 'wb') as fw:
        while True:
            buf = fr.read(16)
            x = AES.block_size - len(buf)
            buf += x.to_bytes(1, 'big') * x
            buf = cipher.encrypt(buf)
            fw.write(buf)
            if x != 0:
                break
    return


def _file_decrypt(src, dest, key, iv):
    key += b'\x00' * (16 - len(key))
    iv += b'\x00' * (16 - len(iv))
    cipher = AES.new(key, AES.MODE_CBC, iv)
    filesize, count = path.getsize(src), 0
    # dest = path.splitext(src)[0] + '(e)' + path.splitext(src)[1]
    with open(src, 'rb') as fr, open(dest, 'wb') as fw:
        while True:
            buf = fr.read(16)
            count += 16
            buf = cipher.decrypt(buf)
            if count == filesize:
                paddingLen = buf[-1]
                fw.write(buf[0:-paddingLen])
                return
            fw.write(buf)


if __name__ == "__main__":
    _file_encrypt('./a.png', './b.png', b'test', b'helloworld')
    _file_decrypt('./b.png', './c.png', b'test', b'helloworld')
