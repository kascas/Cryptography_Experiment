from socket import *
import os
from RSA import *


def register(ip, port):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((ip, port))
    clientSocket.send('reg'.encode('utf-8'))
    print('>>> register')
    n = int(clientSocket.recv(1024).decode('utf-8'), 16)
    e = int(clientSocket.recv(1024).decode('utf-8'), 16)
    username = input('... username: ').encode('utf-8')
    password = RSAES_OAEP_E(n, e, input('... password: ').encode('utf-8'))
    clientSocket.send(username)
    clientSocket.send(password)
    print('... register: ' + clientSocket.recv(1024).decode('utf-8'))
    return


if __name__ == '__main__':
    register('127.0.0.1', 80)
    os.system('pause')
