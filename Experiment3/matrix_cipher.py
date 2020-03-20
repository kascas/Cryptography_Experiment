import os


def matrix_cipher(c, key):
    array, result = [""] * len(key), [""] * len(key)
    for i in range(len(c)):
        array[i % len(key)] += c[i]
    for i in range(len(key)):
        result[ord(key[i]) - ord("1")] += array[i]
    return "".join(result)


if __name__ == "__main__":
    c = input("input plaintext: ")
    key = input("input key: ")
    print(matrix_cipher(c, key))
    os.system("pause")
