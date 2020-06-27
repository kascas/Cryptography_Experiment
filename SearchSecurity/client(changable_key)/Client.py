from socket import *
import os.path
import AESFileEncrypt as aes
from Crypto.Cipher import AES
from aes import *
import WordStat as ws
import time
from RSA import *
from json import *


def tobytes(x, xLen):
    x_array = bytearray(xLen)
    for i in range(xLen):
        x_array[xLen - 1 - i] = x & 0xff
        x >>= 8
    return x_array


def login(clientSocket):
    print('>>> login')
    n = int(clientSocket.recv(1024).decode('utf-8'), 16)
    e = int(clientSocket.recv(1024).decode('utf-8'), 16)
    name = RSAES_OAEP_E(n, e, input('... Username: ').encode('utf-8'))
    pswd = RSAES_OAEP_E(n, e, input('... Password: ').encode('utf-8'))
    clientSocket.send(name)
    clientSocket.send(pswd)
    result = clientSocket.recv(1024).decode('utf-8')
    if result == 'success':
        return True
    elif result == 'failure':
        return False


def _client_upload(clientSocket):
    # filename = input('... File Path: ')
    # find all files in 'File'
    fileList, allFile = [], []
    for a, b, c in os.walk('./File'):
        for i in c:
            fileList.append('./File/' + i)
            allFile.append('./File/' + i)
    # send the number of files
    clientSocket.send(str(len(fileList)).encode('utf-8'))
    with open('Record.json', 'r') as fp:
        d = loads(fp.read())
    # send files and their json-file
    for filename in fileList:
        # get filename without path
        tmp = os.path.split(filename)[1]
        # create a tmp file for encryption
        tmpFile = os.path.split(filename)[0] + '/tmp' + os.path.splitext(filename)[1]
        # get key and iv from PRIVATE.key
        with open('FILE.KEY', 'rb') as fp:
            key = fp.readline().replace(b'\n', b'')
            iv = fp.readline().replace(b'\n', b'')
        # file encrypt
        d[filename.replace('./File/', '')] = [int.from_bytes(key, 'big'), int.from_bytes(iv, 'big')]
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
        time.sleep(0.1)
        # send bloom file
        ws._stat_word(filename)
        clientSocket.send((tmp.split('.')[0] + '.json').encode('utf-8'))
        clientSocket.send(hex(os.path.getsize('./bloom.json')).encode('utf-8'))
        with open('./bloom.json', 'rb') as fp:
            while True:
                data = fp.read(1024)
                if not data:
                    break
                clientSocket.send(data)
        os.remove(tmpFile)
        os.remove('./bloom.json')
        time.sleep(0.1)
        allFile.append(tmp.split('.')[0] + '.json')
        print('... Upload Finish: %s' % filename)
        print('... Upload Finish: %s' % ('./File/' + tmp.split('.')[0] + '.json'))
    with open('Record.json', 'w') as fp:
        fp.write(dumps(d, indent=4))
    return allFile


def _client_search(clientSocket, line):
    fileList, wordList, byteList, num = [], [], [], 0
    # delete all files in folder 'Search'
    for a, b, c in os.walk('./Search'):
        for i in c:
            os.remove('./Search/' + i)
    # send keywords and the number of keywords
    key, mask = getWordKey()
    cipher = AES.new(key, AES.MODE_ECB)

    # get words from line
    wordList = ws._word_extract(line)
    for i in wordList:
        msgList = padding(i.encode('utf-8'))
        for j in msgList:
            byteList.append(j)
    clientSocket.send(str(len(byteList)).encode('utf-8'))
    for i in range(len(byteList)):
        clientSocket.send(cipher.encrypt(byteList[i]))
    print('----------------')
    # get the number of results
    count = int(clientSocket.recv(1024).decode('utf-8'), 10)
    for i in range(count):
        # get file's name and size
        filename = clientSocket.recv(1024).decode('utf-8')
        filesize = int(clientSocket.recv(1024).decode('utf-8'), 16)
        print('... receive:', filename, filesize)
        filecount = 0
        tmpFile = filename.split('.')[0] + '_tmp.' + filename.split('.')[1]
        with open('./Search/' + tmpFile, 'wb') as fp:
            while True:
                data = clientSocket.recv(1024)
                fp.write(data)
                filecount += len(data)
                if filecount == filesize:
                    break
        fileList.append(filename)
    # decrypt tmp files
    with open('Record.json', 'r') as fp:
        d = loads(fp.read())
        for filename in fileList:
            # KeyFolder = d[filename]
            tmpFile = './Search/' + filename.split('.')[0] + '_tmp.' + filename.split('.')[1]
            key_int, iv_int = d[filename][0], d[filename][1]
            key, iv = tobytes(key_int, 16), tobytes(iv_int, 16)
            print(key, iv)
            # get aes's key and iv
            # with open(KeyFolder + '/FILE.KEY', 'rb') as fp:
            #    key = fp.readline()
            #     iv = fp.readline()
            aes._file_decrypt(tmpFile, './Search/' + filename, key, iv)
            os.remove(tmpFile)
    print('... search finish')
    return


def _client_tcp(ip, port):
    # if these two folder do not exist, create them
    if not os.path.exists('./File'):
        os.makedirs('./File')
    if not os.path.exists('./Search'):
        os.makedirs('./Search')
    # login to server
    while True:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((ip, port))
        clientSocket.send('log'.encode('utf-8'))
        if not login(clientSocket):
            print('... <login error>')
        else:
            print('... <login success>')
            break
    # select a mode: upload or search
    while True:
        mode = input('... upload[1] or search[2]: ')
        if mode == '1' or mode == '2':
            break
    print('----------------')
    # send 'mode' to server
    clientSocket.send(mode.encode('utf-8'))
    # 'upload' may send a encrypted file to server
    if mode == '1':
        _client_upload(clientSocket)
    else:
        line = input('... keyword: ')
        _client_search(clientSocket, line)
    clientSocket.close()


if __name__ == '__main__':
    _client_tcp('127.0.0.1', 80)
    os.system('pause')
