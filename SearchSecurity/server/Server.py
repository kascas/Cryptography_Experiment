from socket import *
import json
import os.path
from bloom import *
import time
from RSA import *


def loginVerify(clientSocket):
    n, e, d = rsa_init()
    clientSocket.send(hex(n).encode('utf-8'))
    clientSocket.send(hex(e).encode('utf-8'))
    name = clientSocket.recv(1024).decode('utf-8')
    pswd = clientSocket.recv(1024)
    with open('user.json', 'r') as fp:
        text = fp.read()
    data = json.loads(text)
    value = data.get(name)
    if value == None:
        return 'failure', name
    else:
        if value == RSAES_OAEP_D(n, d, pswd).decode('utf-8'):
            return 'success', name
        else:
            return 'failure', name


def _server_receive(foldername, clientSocket):
    # get the number of files
    filenum = int(clientSocket.recv(1024).decode('utf-8'), 16)
    for i in range(filenum):
        # get file's name and size
        filename = foldername + '/' + clientSocket.recv(1024).decode('utf-8')
        filesize = int(clientSocket.recv(1024).decode('utf-8'), 16)
        print('... upload file: %s    size: %s' % (filename, filesize))
        count = 0
        with open(filename, 'wb') as fp:
            while True:
                data = clientSocket.recv(1024)
                fp.write(data)
                count += len(data)
                if count == filesize:
                    break
        # get file's json-file
        filename = foldername + '/' + clientSocket.recv(1024).decode('utf-8')
        filesize = int(clientSocket.recv(1024).decode('utf-8'), 16)
        count = 0
        print('... upload file: %s    size: %s' % (filename, filesize))
        with open(filename, 'wb') as fp:
            while True:
                data = clientSocket.recv(1024)
                fp.write(data)
                count += len(data)
                if count == filesize:
                    break
    return


def _server_search(clientSocket, foldername):
    fileList, resultList, wordList = [], [], []
    # get keywords
    count = clientSocket.recv(1024)
    for i in range(int(count.decode('utf-8'), 10)):
        data = clientSocket.recv(1024)
        wordList.append(data)
    # print('... KW List: ', wordList)
    # find all json files
    for a, b, c in os.walk(foldername):
        for i in c:
            if i.split('.')[1] == 'json':
                fileList.append(i)
    print('... All Files(BF): ', fileList)
    print('----------------')
    for i in fileList:
        count = 0
        bfname = foldername + '/' + i
        # load bloom's info
        bloom = bloom_read(bfname)
        for j in range(len(wordList)):
            tmp = wordList[j][:]
            if bloom_check(bloom, tmp) == 1:
                count += 1
        if count == len(wordList):
            resultList.append(i.split('.')[0])
        # free bf
        bloom_reset(bloom)
        print('... Check:', bfname)
    print('----------------')
    print('... Result:', resultList)
    return resultList


def _server_return(clientSocket, foldername, resultList):
    # send the number of result-files
    clientSocket.send(str(len(resultList)).encode('utf-8'))
    fileList = []
    # find all result files
    for a, b, c in os.walk(foldername):
        for i in c:
            if i.split('.')[1] != 'json' and (i.split('.')[0] in resultList):
                fileList.append(i)
    # send result files
    for i in fileList:
        filename = foldername + '/' + i
        filesize = os.path.getsize(filename)
        filecount = 0
        print('... Return:', filename, filesize)
        clientSocket.send(i.encode('utf-8'))
        clientSocket.send(hex(filesize).encode('utf-8'))
        with open(filename, 'rb') as fp:
            while True:
                data = fp.read(1024)
                clientSocket.send(data)
                filecount += len(data)
                if filecount == filesize:
                    break
        time.sleep(0.1)
    print('----------------')
    return


def _server_register(clientSocket):
    username = clientSocket.recv(1024).decode('utf-8')
    password = clientSocket.recv(1024).decode('utf-8')
    with open('./User.json', 'r') as fp:
        text = fp.read()
    data = json.loads(text)
    data[username] = password
    with open('./User.json', 'w') as fp:
        js = dumps(data)
        fp.write(js)
    clientSocket.send('success'.encode('utf-8'))
    print('... new user: ')
    print('...     Username: %s' % username)
    print('...     Password: %s' % password)
    return


def _server_tcp():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', 80))
    serverSocket.listen(5)
    if not os.path.exists('./user'):
        os.makedirs('./user')
    while True:
        print('\n>>> waiting for connection')
        clientSocket, clientAddr = serverSocket.accept()
        print('... connected from: ', clientAddr)
        try:
            log_reg = clientSocket.recv(1024).decode('utf-8')
            if log_reg == 'reg':
                _server_register(clientSocket)
                continue
            if log_reg == 'log':
                # user login
                result = loginVerify(clientSocket)
                clientSocket.send(result[0].encode('utf-8'))
                # if login fails, close clientsocket and continue
                if result[0] == 'failure':
                    clientSocket.close()
                    print('<illegal login>')
                    continue
                else:
                    print('... user <%s> login' % result[1])
                # find the user's folder
                foldername = './user/' + result[1]
                if not os.path.exists(foldername):
                    os.makedirs(foldername)
                # receive 'mode' from client
                mode = clientSocket.recv(1024).decode('utf-8')
                # client wants to upload file
                if mode == '1':
                    _server_receive(foldername, clientSocket)
                elif mode == '2':
                    resultList = _server_search(clientSocket, foldername)
                    _server_return(clientSocket, foldername, resultList)
        except ConnectionResetError:
            print('... client\'s connection fails')
        except Exception as r:
            print('error: %s' % r)
        clientSocket.close()
        print('... connection break')
    serverSocket.close()


if __name__ == '__main__':
    _server_tcp()
    os.system('pause')
