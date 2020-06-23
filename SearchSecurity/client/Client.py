from socket import *
import os.path
import AESFileEncrypt as aes
import WordStat as ws
from ctypes import *


def login(clientSocket):
    print('>>> login')
    name = input('... Username: ')
    pswd = input('... Password: ')
    clientSocket.send(name.encode('utf-8'))
    clientSocket.send(pswd.encode('utf-8'))
    result = clientSocket.recv(1024).decode('utf-8')
    if result == 'success':
        return True
    elif result == 'failure':
        return False


def _client_upload(clientSocket):
    # filename = input('... File Path: ')
    fileList = []
    for a, b, c in os.walk('./File'):
        for i in c:
            fileList.append('./File/' + i)
    clientSocket.send(str(len(fileList)).encode('utf-8'))
    for filename in fileList:
        # get filename without path
        tmp = os.path.split(filename)[1]
        # create a tmp file for encryption
        tmpFile = os.path.split(filename)[0] + '/tmp' + os.path.splitext(filename)[1]
        print(tmpFile)
        # get key and iv from PRIVATE.key
        with open('./PRIVATE.key', 'r') as fp:
            key = fp.readline().encode('utf-8')
            iv = fp.readline().encode('utf-8')
        # file encrypt
        aes._file_encrypt(filename, tmpFile, key, iv)
        # send encrypted file
        clientSocket.send(tmp.encode('utf-8'))
        clientSocket.send(hex(os.path.getsize(tmpFile)).encode('utf-8'))
        with open(tmpFile, 'rb') as fp:
            while True:
                data = fp.read(1024)
                if not data:
                    break
                clientSocket.send(data)
        os.remove(tmpFile)
        # send bloom file
        call = cdll.LoadLibrary('./bloom.dll')
        ws._stat_word(call, filename)
        clientSocket.send((tmp.split('.')[0] + '.bf').encode('utf-8'))
        clientSocket.send(hex(os.path.getsize('./bloom.bf')).encode('utf-8'))
        with open('./bloom.bf', 'rb') as fp:
            while True:
                data = fp.read(1024)
                if not data:
                    break
                clientSocket.send(data)
        os.remove('./bloom.bf')
        print('... Upload Finish: %s' % filename)


def _client_search(clientSocket):
    count = input('... number of keywords: ')
    clientSocket.send(str(count).encode('utf-8'))
    for i in range(int(count, 10)):
        msg = input('... keyword: ')
        clientSocket.send(msg.encode('utf-8'))
    count = int(clientSocket.recv(1024), 10)
    for i in range(count):
        result = clientSocket.recv(1024).decode('utf-8')
        print(result)
    return


def _client_tcp(ip, port):
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
        _client_upload(clientSocket)
    else:
        _client_search(clientSocket)
    clientSocket.close()


if __name__ == '__main__':
    _client_tcp('127.0.0.1', 80)
