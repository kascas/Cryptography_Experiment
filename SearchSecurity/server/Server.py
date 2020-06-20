from socket import *
import json
import os.path
from time import ctime


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
    filename = foldername + '/' + clientSocket.recv(1024).decode('utf-8')
    print('... upload file: ', filename)
    with open(filename, 'wb') as fp:
        while True:
            data = clientSocket.recv(1024)
            if len(data) == 0:
                break
            fp.write(data)
    return


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
                while True:
                    msg = clientSocket.recv(1024).decode('utf-8')
                    print('... client: ', msg)
                    if not msg:
                        break
        except ConnectionResetError:
            print('... client\'s connection fails')
        clientSocket.close()
        print('... connection break')
    serverSocket.close()


if __name__ == '__main__':
    _server_tcp()
