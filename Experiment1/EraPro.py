import os
import time


def EraPro(n):
    # to enable this program to run efficiently, divide and multiply operations below will change into bit operations
    # for example, "i>>k" means "i//(2^k)", "i&((1<<k)-1)" means "i%(2^k)"
    # every 128 odds(256 numbers, evens are not allowed) are divided into one group
    list = [0] * ((n >> 8) + 1)
    print(2)
    count=1
    for i in range(3, n + 1, 2):
        # "i" is in the "i//256"th group
        # this odd's position is (i//2)%128
        position = (i >> 1) & ((1 << 7) - 1)
        if ((list[i >> 8] >> position) & 1) != 1:
            print(i)
            count+=1
            for j in range(i * i, n + 1, i):
                if j & 1 == 1:
                    position = (j >> 1) & ((1 << 7) - 1)
                    # set "1" to this position
                    list[j >> 8] |= (1 << position)
    print("total= {}".format(count))


n = int(input("n= "))
start = time.time()
EraPro(n)
end = time.time()
print("time from start to end= {} s".format((end - start)))
os.system("pause")
