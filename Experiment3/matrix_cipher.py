import os


def matrix_cipher(c, key):
    array, result = [""] * len(key), [""] * len(key)
    for i in range(len(c)):
        array[i % len(key)] += c[i]
    for i in range(len(key)):
        result[ord(key[i]) - ord("1")] += array[i]
    return "".join(result)


def de_matrix_cipher(c, key):
    n = len(c) // (len(key))
    array, result, key_I = [""] * len(key), [], []
    for i in range(len(key)):
        for j in range(len(key)):
            if key[j] == chr((i + 1) + ord("0")):
                key_I.append(j)
    for i in range(0, len(key)):
        array[key_I[i]] += c[i * n:(i + 1) * n]
    for i in range(n):
        for j in range(len(key)):
            result.append(array[j][i])
    return "".join(result)


if __name__ == "__main__":
    judge = int(input("please choose [1]crypt, [2]decrypt:  "))
    if (judge == 1):
        c = input("input plaintext: ")
        key = input("input key: ")
        print(matrix_cipher(c, key))
    else:
        c = input("input ciphertext: ")
        key = input("input key: ")
        print(de_matrix_cipher(c, key))
    os.system("pause")
