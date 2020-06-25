from socket import *
import os.path
import AESFileEncrypt as aes
from Crypto.Cipher import AES
from aes import *
import WordStat as ws
import time


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
    # find all files in 'File'
    fileList = []
    for a, b, c in os.walk('./File'):
        for i in c:
            fileList.append('./File/' + i)
    # send the number of files
    clientSocket.send(str(len(fileList)).encode('utf-8'))
    # send files and their json-file
    for filename in fileList:
        # get filename without path
        tmp = os.path.split(filename)[1]
        # create a tmp file for encryption
        tmpFile = os.path.split(filename)[0] + '/tmp' + os.path.splitext(filename)[1]
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
        os.remove('./bloom.json')
        time.sleep(0.1)
        print('... Upload Finish: %s' % filename)
        print('... Upload Finish: %s' % ('./File/' + tmp.split('.')[0] + '.json'))


def _client_search(clientSocket):
    count = input('... number of keywords: ')
    fileList, byteList, num = [], [], 0
    # delete all files in folder 'Search'
    for a, b, c in os.walk('./Search'):
        for i in c:
            os.remove('./Search/' + i)
    # send keywords and the number of keywords
    key, iv = getKey()
    cipher = AES.new(key, AES.MODE_ECB)
    for i in range(int(count, 10)):
        msg = input('... keyword: ').encode('utf-8')
        msgList = padding(msg)
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
    for filename in fileList:
        tmpFile = './Search/' + filename.split('.')[0] + '_tmp.' + filename.split('.')[1]
        # get aes's key and iv
        with open('./PRIVATE.key', 'r') as fp:
            key = fp.readline().encode('utf-8')
            iv = fp.readline().encode('utf-8')
        aes._file_decrypt(tmpFile, './Search/' + filename, key, iv)
        os.remove(tmpFile)
    print('... search finish, quit')
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
        if not login(clientSocket):
            print('... <login error>')
        else:
            print('... <login success>')
            break
    print('----------------')
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
    os.system('pause')
