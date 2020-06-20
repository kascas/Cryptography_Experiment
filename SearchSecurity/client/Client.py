from socket import *
import os.path
import AESFileEncrypt as aes


def login(clientSocket):
    print('>>> login')
    name = input('... name: ')
    pswd = input('... pswd: ')
    clientSocket.send(name.encode('utf-8'))
    clientSocket.send(pswd.encode('utf-8'))
    result = clientSocket.recv(1024).decode('utf-8')
    if result == 'success':
        return True
    elif result == 'failure':
        return False


def _client_upload(clientSocket, filename):
    # get filename without path
    clientSocket.send(os.path.split(filename)[1].encode('utf-8'))
    # create a tmp file
    tmpFile = os.path.split(filename)[0] + '/tmp' + os.path.splitext(filename)[1]
    # get key and iv from PRIVATE.key
    with open('./PRIVATE.key', 'r') as fp:
        key = fp.readline().encode('utf-8')
        iv = fp.readline().encode('utf-8')
    # file encrypt
    aes._file_encrypt(filename, tmpFile, key, iv)
    # send encrypted file
    with open(tmpFile, 'rb') as fp:
        while True:
            data = fp.read(1024)
            if len(data) == 0:
                break
            clientSocket.send(data)
    os.remove(tmpFile)


def _client_search(clientSocket):
    while True:
        msg = input('... send: ')
        clientSocket.send(msg.encode('utf-8'))
        if not msg:
            break
    return


def _client_tcp(ip, port, filename):
    # login to server
    while True:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((ip, port))
        if not login(clientSocket):
            print('<login error>')
        else:
            print('<login success>')
            break
    # select a mode: upload or search
    while True:
        mode = input('upload[1] or search[2]: ')
        if mode == '1' or mode == '2':
            break
    # send 'mode' to server
    clientSocket.send(mode.encode('utf-8'))
    # 'upload' may send a encrypted file to server
    if mode == '1':
        _client_upload(clientSocket, filename)
    else:
        _client_search(clientSocket)
    clientSocket.close()


if __name__ == '__main__':
    _client_tcp('127.0.0.1', 80, './File/1.pdf')
