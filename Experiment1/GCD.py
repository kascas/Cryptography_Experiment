import os


def GCD(a, b):
    #initialize x1,y1,x2,y2
    x1, y1, x2, y2 = 1, 0, 0, 1
    #t1,t2 are temporary variables
    t1, t2 = 0, 0
    L = []
    while (1):
        #copy t1,t2 from x2,y2
        t1, t2 = x2, y2
        #recursion equations
        x2, y2 = x1 - (a // b) * x2, y1 - (a // b) * y2
        #exchange values
        x1, y1 = t1, t2
        if (a % b) == 0:
            break
        #exchange values
        a, b = b, a % b
    #if b is negative,make it positive
    if b < 0:
        b, x1, y1 = (-1) * b, (-1) * x1, (-1) * y1
    L = [b, x1, y1]
    return L


a = int(input("a= "))
b = int(input("b= "))
L = GCD(a, b)
print("gcd(a,b)= {}".format(L[0]))
print("x= {}\ny= {}".format(L[1], L[2]))
print("a*x= " + str(L[1] * a))
print("b*y= " + str(L[2] * b))
os.system("pause")
