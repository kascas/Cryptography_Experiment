from Numtheory import GCD
import os


def CRT(b, m, n):
    # initialize variables
    mm, bm, bmp, result = 1, 0, 0, 0
    # compute mm=m1*m2*...*mn
    for i in range(n):
        mm *= m[i]
    # compute bm=mm/mi, bmp*bm mod mi=1
    for i in range(n):
        bm = mm // m[i]
        bmp = GCD(bm, m[i])[1]
        result = (result + bm * bmp * b[i]) % mm
    # if result is negative, make it positive
    if result <= 0:
        result = ((result * (-1)) // mm + 1) * mm + result
    return result


b = []
m = []
n = int(input("num of CRT is: "))
# input values for args
for i in range(n):
    print("m_{}= ".format(i), end="")
    m.append(int(input()))
for i in range(n):
    print("b_{}= ".format(i), end="")
    b.append(int(input()))
result = CRT(b, m, n)
print("result= {}".format(result))
os.system("pause")
