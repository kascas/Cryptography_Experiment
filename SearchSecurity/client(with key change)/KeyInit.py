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
    KeyFolder = './Keys/' + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    if not os.path.exists(KeyFolder):
        os.makedirs(KeyFolder)
    FileKeyinit(KeyFolder)
    # WordKeyInit(KeyFolder)
    # with open('Record.json', 'w') as fp:
    #    fp.write('{\"test\":\"test\"}')
    return


if __name__ == "__main__":
    KeyInit()
    print('... key init finish')
    os.system('pause')
