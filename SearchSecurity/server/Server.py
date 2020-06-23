from socket import *
import json
import os.path
from time import ctime
from ctypes import *
import BloomFilter as BF


def loginVerify(clientSocket):
    name = clientSocket.recv(1024).decode('utf-8')
    pswd = clientSocket.recv(1024).decode('utf-8')
    with open('user.json', 'r') as fp:
        text = fp.read()
    data = json.loads(text)
    value = data.get(name)
    if value == None:
        return 'failure', name
    else:
        if value == pswd:
            return 'success', name
        else:
            return 'failure', name


def _server_receive(foldername, clientSocket):
    filenum = int(clientSocket.recv(1024).decode('utf-8'), 16)
    for i in range(filenum):
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
    call = cdll.LoadLibrary('./bloom.dll')
    fileList, resultList, wordList = [], [], []
    count = clientSocket.recv(1024)
    for i in range(int(count.decode('utf-8'), 10)):
        data = clientSocket.recv(1024)
        wordList.append(data.decode('utf-8'))
    print('... KW List: ', wordList)
    for a, b, c in os.walk(foldername):
        for i in c:
            if i.split('.')[1] == 'bf':
                fileList.append(i)
    print('... All Files(BF): ', fileList)
    for i in fileList:
        count = 0
        bfname = foldername + '/' + i
        BF._bloom_read(call, bfname.encode('utf-8'))
        for j in range(len(wordList)):
            tmp = wordList[j][:]
            if BF._bloom_check(call, tmp) == 1:
                count += 1
        if count == len(wordList):
            resultList.append(i.split('.')[0])
        BF._bloom_delete(call)
        print(bfname)
    clientSocket.send(str(len(resultList)).encode('utf-8'))
    for i in resultList:
        clientSocket.send(i.encode('utf-8'))
    return resultList


def _server_tcp():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', 80))
    serverSocket.listen(5)
    while True:
        print('\n>>> waiting for connection')
        clientSocket, clientAddr = serverSocket.accept()
        print('... connected from: ', clientAddr)
        try:
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
                _server_search(clientSocket, foldername)
                '''
                while True:
                    
                    msg = clientSocket.recv(1024).decode('utf-8')
                    print('... client: ', msg)
                    if not msg:
                        break
                '''
        except ConnectionResetError:
            print('... client\'s connection fails')
        except Exception as r:
            print('error: %s' % r)
        clientSocket.close()
        print('... connection break')
    serverSocket.close()


if __name__ == '__main__':
    _server_tcp()
