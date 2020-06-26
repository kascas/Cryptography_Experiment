import tkinter as tk
from tkinter.filedialog import *
import os.path
import Client as client
import tkinter.messagebox
from socket import *
import os.path
from RSA import *

root = tk.Tk()
root.title("Searchable Encryption")
root.geometry("720x560")

clientSocket = socket(AF_INET, SOCK_STREAM)

username = StringVar()
password = StringVar()
ip = StringVar()
port = IntVar()
ip_value = ''
port_value = 0
fileList = []


def get_all_files():
    fileList = []
    for a, b, c in os.walk('./File'):
        for i in c:
            fileList.append(i)
    return fileList


def print_all_files():
    fileList = get_all_files()
    for file in fileList:
        text_1.insert('insert', 'File/' + file + '\n')
    text_1.config(state='disabled')
    return


def get_search_files():
    fileList = []
    for a, b, c in os.walk('./Search'):
        for i in c:
            fileList.append(i)
    return fileList


def print_search_files():
    fileList = get_search_files()
    for file in fileList:
        text_2.insert('insert', 'Search/' + file + '\n')
    text_2.config(state='disabled')
    return


def _connect_():
    global clientSocket
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        ip_value = ip.get()
        port_value = port.get()
        clientSocket.connect((ip_value, port_value))
    except Exception as s:
        tkinter.messagebox.showinfo('note', 'connection failure')
        print(s)
        return
    tkinter.messagebox.showinfo('note', 'connection success')
    ip_entry['state'] = 'disabled'
    port_entry['state'] = 'disabled'
    return


def _connect_without_msgbox():
    global clientSocket
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        ip_value = ip.get()
        port_value = port.get()
        clientSocket.connect((ip_value, port_value))
    except Exception as s:
        print(s)
        return
    ip_entry['state'] = 'disabled'
    port_entry['state'] = 'disabled'
    return


def _login_():
    global clientSocket
    clientSocket.send('log'.encode('utf-8'))
    n = int(clientSocket.recv(1024).decode('utf-8'), 16)
    e = int(clientSocket.recv(1024).decode('utf-8'), 16)
    name = username.get()
    pswd = RSAES_OAEP_E(n, e, password.get().encode('utf-8'))
    clientSocket.send(name.encode('utf-8'))
    clientSocket.send(pswd)
    result = clientSocket.recv(1024).decode('utf-8')
    if result == 'success':
        password_entry['state'] = 'disabled'
        username_entry['state'] = 'disabled'
        tkinter.messagebox.showinfo('note', 'login success')
        return True
    elif result == 'failure':
        tkinter.messagebox.showinfo('note', 'login failure')
        _connect_without_msgbox()
        return False


def _login_without_msgbox():
    global clientSocket
    clientSocket.send('log'.encode('utf-8'))
    n = int(clientSocket.recv(1024).decode('utf-8'), 16)
    e = int(clientSocket.recv(1024).decode('utf-8'), 16)
    name = username.get()
    pswd = RSAES_OAEP_E(n, e, password.get().encode('utf-8'))
    clientSocket.send(name.encode('utf-8'))
    clientSocket.send(pswd)
    result = clientSocket.recv(1024).decode('utf-8')
    if result == 'success':
        password_entry['state'] = 'disabled'
        username_entry['state'] = 'disabled'
        return True
    elif result == 'failure':
        _connect_without_msgbox()
        return False


def _upload_():
    clientSocket.send('1'.encode('utf-8'))
    uploadfile = []
    text_3['state'] = 'normal'
    text_3.delete('0.0', END)
    try:
        uploadfile = client._client_upload(clientSocket)
    except Exception:
        tkinter.messagebox.showinfo('note', 'upload failes, try again')
    for file in uploadfile:
        text_3.insert('insert', file.replace('./File/', '') + '\n')
    tkinter.messagebox.showinfo('note', 'upload success')
    text_3['state'] = 'disabled'
    clientSocket.close()
    _connect_without_msgbox()
    _login_without_msgbox()
    return


def _search_():
    text_2['state'] = 'normal'
    text_2.delete('0.0', END)
    clientSocket.send('2'.encode('utf-8'))
    line = search_text.get('0.0', END)
    try:
        client._client_search(clientSocket, line)
    except Exception:
        tkinter.messagebox.showinfo('note', 'search failes, try again')
    print_search_files()
    text_2['state'] = 'disabled'
    tkinter.messagebox.showinfo('note', 'search success')
    clientSocket.close()
    _connect_without_msgbox()
    _login_without_msgbox()
    return


port.set(80)
ip_label = tk.Label(root, text="Ip Addr", font=("宋体", 10))
ip_entry = tk.Entry(root, textvariable=ip, show=None, font=("宋体", 10), width="20")
port_label = tk.Label(root, text="Port", font=("宋体", 10))
port_entry = tk.Entry(root, textvariable=port, show=None, font=("宋体", 10), width="20")

ip_label.place(x=240, y=32)
ip_entry.place(x=320, y=32)
port_label.place(x=240, y=64)
port_entry.place(x=320, y=64)

tcp_button = tk.Button(root, text="connect", width="10", height=1, command=_connect_)
tcp_button.place(x=320, y=96)

username_label = tk.Label(root, text="Userword", font=("宋体", 10))
username_entry = tk.Entry(root, textvariable=username, show=None, font=("Arial", 10), width="20")
password_label = tk.Label(root, text="Password", font=("宋体", 10))
password_entry = tk.Entry(root, textvariable=password, show=None, font=("Arial", 10), width="20")

username_label.place(x=240, y=160)
username_entry.place(x=320, y=160)
password_label.place(x=240, y=192)
password_entry.place(x=320, y=192)

login_button = tk.Button(root, text="login", width="10", height=1, command=_login_)
login_button.place(x=320, y=218)

upload_button = tk.Button(root, text="Upload", width="10", height=1, command=_upload_)
upload_button.place(x=240, y=480)

search_button = tk.Button(root, text="Search", width="10", height=1, command=_search_)
search_button.place(x=380, y=480)

search_label = tk.Label(root, text="KeyWord", font=("宋体", 10))
search_text = tk.Text(root, height=3, width=20, font=("宋体", 10))
search_label.place(x=240, y=280)
search_text.place(x=320, y=280)

label_1 = tk.Label(root, text="Files in folder \'./File\'", font=("宋体", 10))
label_1.place(x=16, y=16)
frame_1 = tk.Frame(root)
scroll_1 = tk.Scrollbar(frame_1)
text_1 = tk.Text(frame_1, height=36, width=24, font=("宋体", 10))
scroll_1.pack(side=tk.RIGHT, fill=tk.Y)
text_1.config(yscrollcommand=scroll_1.set)
text_1.pack(side=tk.LEFT)
scroll_1.config(command=text_1.yview)
frame_1.place(x=16, y=48)
print_all_files()

label_2 = tk.Label(root, text="Search result", font=("宋体", 10))
label_2.place(x=512, y=16)
frame_2 = tk.Frame(root)
scroll_2 = tk.Scrollbar(frame_2)
text_2 = tk.Text(frame_2, height=36, width=24, font=("宋体", 10), state='disabled')
scroll_2.pack(side=tk.RIGHT, fill=tk.Y)
text_2.config(yscrollcommand=scroll_2.set)
text_2.pack(side=tk.LEFT)
scroll_2.config(command=text_2.yview)
frame_2.place(x=512, y=48)

label_3 = tk.Label(root, text="Upload", font=("宋体", 10))
label_3.place(x=240, y=350)
frame_3 = tk.Frame(root)
scroll_3 = tk.Scrollbar(frame_3)
text_3 = tk.Text(frame_3, height=8, width=20, font=("宋体", 10), state='disabled')
scroll_3.pack(side=tk.RIGHT, fill=tk.Y)
text_3.config(yscrollcommand=scroll_3.set)
text_3.pack(side=tk.LEFT)
scroll_3.config(command=text_3.yview)
frame_3.place(x=320, y=350)

root.mainloop()
