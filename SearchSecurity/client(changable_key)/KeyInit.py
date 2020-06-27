import secrets
import os
import datetime
import shutil


def FileKeyinit(KeyFolder):
    key = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    filename = KeyFolder + '/FILE.KEY'
    with open(filename, 'wb') as fp:
        fp.write(key)
        fp.write(b'\n')
        fp.write(iv)
        fp.write(b'\n')
        fp.write(KeyFolder.encode('utf-8'))
    shutil.copy(filename, 'FILE.KEY')
    return


def WordKeyInit(KeyFolder):
    word_key = secrets.token_bytes(16)
    mask = secrets.token_bytes(16)
    filename = KeyFolder + '/WORD.KEY'
    with open(filename, 'wb') as fp:
        fp.write(word_key)
        fp.write(b'\n')
        fp.write(mask)
        fp.write(b'\n')
        fp.write(KeyFolder.encode('utf-8'))
    shutil.copy(filename, 'WORD.KEY')
    return


def KeyInit():
    key = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    with open('FILE.KEY', 'wb') as fp:
        fp.write(key)
        fp.write(b'\n')
        fp.write(iv)
    return


if __name__ == "__main__":
    KeyInit()
    print('... key init finish')
    os.system('pause')
