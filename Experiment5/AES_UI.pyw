import os
import tkinter as tk
from AES import *


def AES_crypt():
    p, key, crypt_result = int(text_in.get(), 16), int(key_in.get(), 16), 0
    result_text.delete(1.0, tk.END)
    if len(hex(key).replace("0x", "")) <= 32:
        Nk = 4
    elif len(hex(key).replace("0x", "")) <= 48:
        Nk = 6
    elif len(hex(key).replace("0x", "")) <= 64:
        Nk = 8
    else:
        result_text.insert(1.0, "KeyLen > 256")
        return
    key_list = KeyExpansion(key, Nk, NrComputer(Nk), 1)
    crypt_result = AES(p, key_list, 1, Nk)
    result_text.insert(1.0, hex(crypt_result).replace("0x", "").zfill(32))
    return


def AES_decrypt():
    p, key, decrypt_result = int(text_in.get(), 16), int(key_in.get(), 16), 0
    result_text.delete(1.0, tk.END)
    if len(hex(key).replace("0x", "")) <= 32:
        Nk = 4
    elif len(hex(key).replace("0x", "")) <= 48:
        Nk = 6
    elif len(hex(key).replace("0x", "")) <= 64:
        Nk = 8
    else:
        result_text.insert(1.0, "KeyLen > 256")
        return
    key_list = KeyExpansion(key, Nk, NrComputer(Nk), 2)
    decrypt_result = AES(p, key_list, 2, Nk)
    result_text.insert(1.0, hex(decrypt_result).replace("0x", "").zfill(32))
    return


root = tk.Tk()
root.title("AES")
root.geometry("600x200")

input_frame = tk.Frame(root)
input_frame.pack()

text_frame = tk.Frame(input_frame).pack()
text_label = tk.Label(text_frame, text="content", font=("Arial", 12))
text_in = tk.Entry(text_frame, show=None, font=("Arial", 10), width="64")

key_frame = tk.Frame(input_frame).pack()
key_label = tk.Label(key_frame, text="key", font=("Arial", 12))
key_in = tk.Entry(key_frame, show=None, font=("Arial", 10), width="64")

crypt_button = tk.Button(root, text="Crpyt!", width="10", command=AES_crypt)
decrypt_button = tk.Button(root, text="Decrypt!", width="10", command=AES_decrypt)
result_label = tk.Label(root, text="result", font=("Arial", 12))
result_text = tk.Text(root, height="1", width="64", font=("Arial", 10))

text_label.place(x=40, y=25)
text_in.place(x=120, y=25)
key_label.place(x=40, y=60)
key_in.place(x=120, y=60)
crypt_button.place(x=390, y=90)
decrypt_button.place(x=490, y=90)
result_label.place(x=40, y=150)
result_text.place(x=120, y=150)

root.mainloop()
