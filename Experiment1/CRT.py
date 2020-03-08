from numtheory import GCD


def CRT(b, m, n):
    mm = 1;
    bm = 0;
    bmp = 0;
    result = 0;
    temp = 0
    for i in range(n):
        mm *= m[i]
    for i in range(n):
        bm = mm // m[i]
        bmp = GCD(bm, m[i])[1]
        temp = bm * bmp * b[i]
        result = (result + temp) % mm
    if result < 0:
        temp = (result * (-1)) // mm + 1
        result = temp * mm + result
    return result


b = [];
m = []
n = int(input("num of CRT is: "))
for i in range(n):
    print("m_{}= ".format(i), end="")
    m.append(int(input()))
for i in range(n):
    print("b_{}= ".format(i), end="")
    b.append(int(input()))
result = CRT(b, m, n)
print("result= {}".format(result))
