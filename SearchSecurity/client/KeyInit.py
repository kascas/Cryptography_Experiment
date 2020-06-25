import secrets


def keyinit():
    key = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    with open('AES.KEY', 'wb') as fp:
        fp.write(key)
        fp.write(b'\n')
        fp.write(iv)
    return


if __name__ == "__main__":
    keyinit()
