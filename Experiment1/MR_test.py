import random
import os
from Numtheory import FastExp


def MR_test(p, r):
    #p_1 is p-1, initialize variables
    pt = p_1 = p - 1
    temp, k, judge = 2, 0, 0
    #compute k,q s.t. p-1=q*(2^k)
    while (pt % temp) == 0:
        temp *= 2
        k += 1
    #temp=(p-1)/q which equals 2^k
    temp = temp // 2
    q = p_1 // temp
    print("r= {}".format(r), end="    ")
    #compute r^q mod p
    r_q = FastExp(r, q, p)
    if (r_q == 1):
        print("True")
        return 0
    else:
        temp = 1
        #exp is q*(2^j)
        for j in range(k):
            exp = temp * q
            r_q = FastExp(r, exp, p)
            if (r_q == p - 1):
                print("True")
                return 0
            temp *= 2
        print("False")
        return 1


p = int(input("p= "))
num = int(input("how many times do you want to test: "))
r_list = []
judge = 0
for i in range(num):
    while (1):
        k = 0
        r = random.randint(2, p - 1)
        for j in range(len(r_list)):
            if r_list[j] == r:
                k += 1
        if (k == 0):
            break
    r_list.append(r)
    judge += MR_test(p, r)
if (judge == 0):
    print(">>> True")
else:
    print(">>> False")
os.system("pause")
