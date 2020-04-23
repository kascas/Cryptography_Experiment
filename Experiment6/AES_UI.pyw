import os
import tkinter as tk
from tkinter.filedialog import *
from ctypes import *


def encrypt():
    call = cdll.LoadLibrary('./AES.dll')
    key_string, IV_string = key_entry.get(), IV_entry.get()

    k, keylen = (c_int8 * 16)(0), 0
    if len(key_string) <= 16:
        keylen = len(key_string)
    else:
        keylen = 16

    IV, IVlen = (c_int8 * 16)(0), 0
    if len(IV_string) <= 16:
        IVlen = len(IV_string)
    else:
        IVlen = 16

    for i in range(keylen):
        k[i] = ord(key_string[i])
    for i in range(IVlen):
        IV[i] = ord(IV_string[i])

    if v.get() == 1:
        call.AES_ECB_encrypt(bytes(src_path.get(), 'utf-8'), bytes(dest_path.get(), 'utf-8'), k)
    elif v.get() == 2:
        call.AES_CBC_encrypt(bytes(src_path.get(), 'utf-8'), bytes(dest_path.get(), 'utf-8'), k, IV)
    elif v.get() == 3:
        call.AES_OFB_encrypt(bytes(src_path.get(), 'utf-8'), bytes(dest_path.get(), 'utf-8'), k, IV)
    elif v.get() == 4:
        call.AES_CFB_encrypt(bytes(src_path.get(), 'utf-8'), bytes(dest_path.get(), 'utf-8'), k, IV)

    return


def decrypt():
    call = cdll.LoadLibrary('./AES.dll')
    key_string, IV_string = key_entry.get(), IV_entry.get()

    k, keylen = (c_int8 * 16)(0), 0
    if len(key_string) <= 16:
        keylen = len(key_string)
    else:
        keylen = 16

    IV, IVlen = (c_int8 * 16)(0), 0
    if len(IV_string) <= 16:
        IVlen = len(IV_string)
    else:
        IVlen = 16

    for i in range(keylen):
        k[i] = ord(key_string[i])
    for i in range(IVlen):
        IV[i] = ord(IV_string[i])

    if v.get() == 1:
        call.AES_ECB_decrypt(bytes(src_path.get(), 'utf-8'), bytes(dest_path.get(), 'utf-8'), k)
    elif v.get() == 2:
        call.AES_CBC_decrypt(bytes(src_path.get(), 'utf-8'), bytes(dest_path.get(), 'utf-8'), k, IV)
    elif v.get() == 3:
        call.AES_OFB_decrypt(bytes(src_path.get(), 'utf-8'), bytes(dest_path.get(), 'utf-8'), k, IV)
    elif v.get() == 4:
        call.AES_CFB_decrypt(bytes(src_path.get(), 'utf-8'), bytes(dest_path.get(), 'utf-8'), k, IV)

    return


def get_src_path():
    path = askopenfilename(initialdir="C:/Users/DELL/Desktop")
    src_path.set(path)
    return


def get_dest_path():
    path = askopenfilename(initialdir="C:/Users/DELL/Desktop")
    dest_path.set(path)
    return


root = tk.Tk()
root.title("AES")
root.geometry("600x240")

src_path = StringVar()
dest_path = StringVar()

src_label = tk.Label(root, text="src ", font=("Arial", 12))
src_entry = tk.Entry(root, textvariable=src_path, show=None, font=("Arial", 10), width="56")
src_file = tk.Button(root, text="...", width="5", height=1, command=get_src_path)

dest_label = tk.Label(root, text="dest", font=("Arial", 12))
dest_entry = tk.Entry(root, textvariable=dest_path, show=None, font=("Arial", 10), width="56")
dest_file = tk.Button(root, text="...", width="5", height=1, command=get_dest_path)

key_label = tk.Label(root, text="key ", font=("Arial", 12))
key_entry = tk.Entry(root, show=None, font=("Arial", 10), width="24")

IV_label = tk.Label(root, text="IV ", font=("Arial", 12))
IV_entry = tk.Entry(root, show=None, font=("Arial", 10), width="24")

v = tk.IntVar()
v.set(1)

ECB = tk.Radiobutton(root, variable=v, text="ECB", value=1)
CBC = tk.Radiobutton(root, variable=v, text="CBC", value=2)
OFB = tk.Radiobutton(root, variable=v, text="OFB", value=3)
CFB = tk.Radiobutton(root, variable=v, text="CFB", value=4)
CRT = tk.Radiobutton(root, variable=v, text="CRT", value=5)

crypt_button = tk.Button(root, text="Crpyt!", width="10", command=encrypt)
decrypt_button = tk.Button(root, text="Decrypt!", width="10", command=decrypt)

src_label.place(x=40, y=30)
src_entry.place(x=80, y=30)
dest_label.place(x=40, y=65)
dest_entry.place(x=80, y=65)
src_file.place(x=525, y=25)
dest_file.place(x=525, y=60)
key_label.place(x=40, y=100)
key_entry.place(x=80, y=100)
IV_label.place(x=265, y=100)
IV_entry.place(x=305, y=100)
ECB.place(x=60, y=160)
CBC.place(x=120, y=160)
OFB.place(x=180, y=160)
CFB.place(x=240, y=160)
CRT.place(x=300, y=160)
crypt_button.place(x=390, y=160)
decrypt_button.place(x=490, y=160)

root.mainloop()
