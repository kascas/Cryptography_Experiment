import secrets
import os


def FileKeyinit():
    key = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    with open('FILE.KEY', 'wb') as fp:
        fp.write(key)
        fp.write(b'\n')
        fp.write(iv)
    return


def WordKeyInit():
    word_key = secrets.token_bytes(16)
    with open('WORD.KEY', 'wb') as fp:
        fp.write(word_key)
    return


if __name__ == "__main__":
    FileKeyinit()
    WordKeyInit()
    print('... key init finish')
    os.system('pause')
