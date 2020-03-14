import os


def trans(n, type):
    return int(n, int(type))


def GF_plus(a, b, n=int("0b100011011", 2)):
    return a ^ b


def GF_minus(a, b, n=int("0b100011011", 2)):
    return a ^ b


def GF_multi(a, b, n=int("0b100011011", 2)):
    result, temp= 0, a
    while (b != 0):
        if (b & 1) == 1:
            result = result ^ temp
        # temp = f(x) * (x ^ k)
        temp = temp << 1
        # if a7==1, then mod n to make deg(f(x)*(x^k))<8
        if (temp >> 8) & 1 == 1:
            temp = temp ^ n
        #print(bin(temp).replace("0b","").zfill(8))
        #do right-move to b
        b = b >> 1
    return result


def GF_mod(a, b):
    temp, move = b, 0
    while (temp < a):
        temp = temp << 1
        move += 1
    while (a > b):
        a = a ^ (b << move)
        move -= 1
    return ()


'''
n_temp, type = input("input n and its type= ").split()
n = trans(n_temp, type)
'''
a_temp, type = input("input a and its type= ").split()
a = trans(a_temp, type)
b_temp, type = input("input b and its type= ").split()
b = trans(b_temp, type)
print("GF_plus= " + bin(GF_plus(a, b)).replace("0b", ""))
print("GF_minus= " + bin(GF_minus(a, b)).replace("0b", ""))
print("GF_multi= " + bin(GF_multi(a, b)).replace("0b", ""))
# print("GF_mod= " + bin(GF_mod(a, b)).replace("0b", ""))

os.system("pause")
