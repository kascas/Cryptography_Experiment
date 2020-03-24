import os


def LFA(c):
    # single-letter mode
    dict = Single_Letter(c)
    print("as for single-letter mode, result is: \n" + "".join(de_Trans(c, dict)))
    # double-letter mode
    result = Double_Letter(c, dict)
    if result != {}:
        dict = result
    plaintext = de_Trans(c, dict)
    print(">>>ciphertext: " + c)
    print(">>>plaintext : " + "".join(plaintext))
    print("<input \"quit\" to end this program>")
    while (1):
        readin = input("  key-value to change: ")
        if (readin != "quit"):
            key, value = readin.split(":")
        else:
            break
        plaintext = []
        dict = ChangeDict(dict, key, value)
        for i in range(len(c)):
            if c[i] == ' ':
                plaintext.append(' ')
            else:
                plaintext.append(dict[c[i]])
        print(">>>ciphertext: " + c)
        print(">>>plaintext : " + "".join(plaintext))
    return ("".join(plaintext), dict)


def ChangeDict(dict, key, value):
    pos = ""
    for i, j in dict.items():
        if j == value:
            pos = i
            break
    dict[key], dict[pos] = value, dict[key]
    return dict


def Single_Letter(c):
    statistics = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0,
                  'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0,
                  'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0,
                  'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0,
                  'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
    frequency = ['e', 't', 'a', 'o', 'i',
                 'n', 's', 'h', 'r', 'd',
                 'l', 'c', 'u', 'm', 'w',
                 'f', 'g', 'y', 'p', 'b',
                 'v', 'k', 'j', 'x', 'q', 'z']
    dict = statistics
    # compute the number of each letter
    for i in range(len(c)):
        if c[i] != ' ':
            dict[c[i]] += 1
    # do sorted operation to letters
    statistics = sorted(dict, key=dict.__getitem__, reverse=True)
    # create a dict to record letter-mapping
    for i in range(26):
        dict[statistics[i]] = frequency[i]
    # print("Single-letter: {}".format(dict))
    return dict


def Double_Letter(c, dict):
    double_letter = ["is", "of", "in", "on", "it", "he", "me", "at", "by", "us", "to", "my", "if", "go", "by", "do",
                     "no", "or", "so", "we"]
    string, dict_list, phrase = c.split(" "), [], []
    print("according to double-letter, choose from following sentences: ")
    # select a double-letter-word
    for i in range(len(string)):
        if len(string[i]) == 2:
            phrase.append(string[i])
    if len(phrase) == 0:
        print("no double-letter-word")
        return {}
    # recording the mapping for each situation
    dict_k = dict.copy()
    for k in range(len(phrase)):
        for i in range(len(double_letter)):
            dict_temp = dict_k.copy()
            print("{:2}: ".format(i + 1), end="")
            dict_temp = ChangeDict(dict_temp, phrase[k][0], double_letter[i][0])
            dict_temp = ChangeDict(dict_temp, phrase[k][1], double_letter[i][1])
            dict_list.append(dict_temp)
            for j in range(len(c)):
                if c[j] == ' ':
                    print(" ", end="")
                else:
                    print(dict_temp[c[j]], end="")
            print()
        select = int(input("select one to continue: "))
        dict_k, dict_list = dict_list[select - 1].copy(), []
    return dict_k


def de_Trans(c, dict):
    plaintext = []
    for i in range(len(c)):
        if c[i] == ' ':
            plaintext.append(' ')
        else:
            plaintext.append(dict[c[i]])
    return plaintext


if __name__ == "__main__":
    c = input("input ciphertext: ").lower()
    plaintext, dict = LFA(c)
    print("plaintext is: {}".format(plaintext))
    print("dict is: {}".format(dict))
    os.system("pause")
