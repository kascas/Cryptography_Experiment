import os


def trans(n, type):
    return int(n, int(type))


def GF_plus(a, b, n=int("0b100011011", 2)):
    return a ^ b


def GF_minus(a, b, n=int("0b100011011", 2)):
    return a ^ b


def GF_multi(a, b, n=int("0b100011011", 2)):
    result = 0
    while (b != 0):
        if (b & 1) == 1:
            result = result ^ a
        # a = f(x) * (x ^ k)
        a = a << 1
        # it's known that "x^n mod p(x)=p(x)-x^n"
        # if a7==1, then mod n to make deg(f(x)*(x^k))<8
        if (a >> 8) & 1 == 1:
            a = a ^ n
        # do right-move to b
        b = b >> 1
        # print(bin(a).replace("0b","").zfill(8))
    return result


def GF_div(a, b):
    quo, re = 0, 0
    while (a > b):
        move = len(bin(a)) - len(bin(b))
        a = a ^ (b << move)
        quo += (1 << move)
    return (quo, a)


'''
n_temp, type = input("input n and its type= ").split()
n = trans(n_temp, type)
'''
if __name__ == "__main__":
    a_temp, type = input("input a and its type= ").split()
    a = trans(a_temp, type)
    b_temp, type = input("input b and its type= ").split()
    b = trans(b_temp, type)
    print("GF_plus= " + bin(GF_plus(a, b)).replace("0b", ""))
    print("GF_minus= " + bin(GF_minus(a, b)).replace("0b", ""))
    print("GF_multi= " + bin(GF_multi(a, b)).replace("0b", ""))
    print("quo GF_div= " + bin(GF_div(a, b)[0]).replace("0b", ""))
    print("mod GF_div= " + bin(GF_div(a, b)[1]).replace("0b", ""))
    os.system("pause")
