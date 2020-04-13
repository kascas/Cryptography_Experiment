import os
import time
from AES_basic import *


class AES():
    def __init__(self, key, mode, IV=0x0):
        self.key = key
        self.IV = IV
        self.mode = 0
        if mode == "ECB":
            self.mode = 1
        elif mode == "CBC":
            self.mode = 2
        elif mode == "OFB":
            self.mode = 3
        elif mode == "CFB":
            self.mode = 4
        elif mode == "CRT":
            self.mode = 5

    def pkcs_7(self, filepath):
        with open(filepath, "rb") as fp:
            filelen = os.path.getsize(filepath)
            content, paddinglen = fp.read(), 16 - (filelen % 16)
        value = paddinglen.to_bytes(1, 'big')
        content += (value * paddinglen)
        content_array = []
        for i in range(len(content) // 16):
            content_array.append(content[i * 16:i * 16 + 16])
        fp.close()
        return content_array

    def file_to_group(self, filepath):
        with open(filepath, "rb") as fp:
            content, content_array = open(filepath, "rb").read(), []
        print(content)
        for i in range(len(content) // 16):
            content_array.append(content[i * 16:i * 16 + 16])
        return content_array

    def delete_padding(self, content):
        return content[:len(content) - content[-1]]

    def file_encrypt(self, filepath, output="new"):
        result, extension_name = b'', os.path.splitext(filepath)[1]
        output += extension_name
        if self.mode == 1:
            result = self.ECB_encrypt(filepath)
        '''
        elif self.mode == 2:
            result = self.CBC_encrypt(filepath)
        elif self.mode == 3:
            result = self.OFB_encrypt(filepath)
        elif self.mode == 4:
            result = self.CFB_encrypt(filepath)
        elif self.mode == 5:
            result = self.CRT_encrypt(filepath)
        '''
        with open(output, "wb") as f_out:
            f_out.write(result)
        return result

    def file_decrypt(self, filepath, output="new"):
        result, extension_name = b'', os.path.splitext(filepath)[1]
        output += extension_name
        if self.mode == 1:
            result = self.ECB_decrypt(filepath)
        print(result)
        '''
        elif self.mode == 2:
            result = self.CBC_decrypt(filepath)
        elif self.mode == 3:
            result = self.OFB_decrypt(filepath)
        elif self.mode == 4:
            result = self.CFB_decrypt(filepath)
        elif self.mode == 5:
            result = self.CRT_decrypt(filepath)
        return result
        '''
        with open(output, "wb") as f_out:
            f_out.write(result)
        return result

    def ECB_encrypt(self, filepath):
        content_array, result_bytes = self.pkcs_7(filepath), b''
        for i in range(len(content_array)):
            result_bytes += encrypt(bytearray(content_array[i]), self.key)
        return result_bytes

    def ECB_decrypt(self, filepath):
        content_array, tmp_bytes = self.file_to_group(filepath), b''
        for i in range(len(content_array)):
            tmp_bytes += decrypt(bytearray(content_array[i]), self.key)
        result_bytes = self.delete_padding(tmp_bytes)
        return result_bytes


if __name__ == "__main__":
    obj = AES(0x0123456789abcdeffedcba9876543210, 'ECB', 0)
    print(obj.file_encrypt("a.png", "out"))
    print(obj.file_decrypt("out.png", "new"))
