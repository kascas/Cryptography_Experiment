import os


def Vernam(f_in, f_out, key):
    s_read = f_in.read()
    L = []
    for i in range(len(s_read)):
        L.append(bin(ord(s_read[i]) ^ ord(key[i % len(key)])).replace("0b", "").zfill(8))
        print(chr(ord(s_read[i]) ^ ord(key[i % len(key)])))
    s_write = "".join(L)
    f_out.write(s_write)
    f_in.close()
    f_out.close()
    return


# f_in_path = input("input path for input: ")
# f_out_path = input("input path for output: ")
f_in_path, f_out_path = "input1.txt", "output1.txt"
f_in, f_out = open(f_in_path, mode="r"), open(f_out_path, mode="w")
key = input("input key: ")
Vernam(f_in, f_out, key)
