from socket import *
import os


def register(ip, port):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((ip, port))
    clientSocket.send('reg'.encode('utf-8'))
    print('>>> register')
    username = input('... username: ').encode('utf-8')
    password = input('... password: ').encode('utf-8')
    clientSocket.send(username)
    clientSocket.send(password)
    print(clientSocket.recv(1024).decode('utf-8'))
    return


if __name__ == '__main__':
    register('127.0.0.1', 80)
    os.system('pause')
