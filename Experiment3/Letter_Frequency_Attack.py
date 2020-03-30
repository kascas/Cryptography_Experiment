import os
import itertools
import copy


def LFA(c):
    # Single_Letter test
    dict, stat, freq = Single_Letter(c)
    '''
    stat_combine = list(itertools.permutations(stat[:6], 6))
    freq_combine = list(freq[:6])
    for i in range(len(stat_combine)):
        temp = copy.copy(dict)
        for j in range(6):
            temp = ChangeDict(temp, stat_combine[i][j], freq_combine[j])
        print("".join(de_Trans(c, temp)))
    '''
    L = input("input word you want to test: ").split(" ")
    '''
    print("dict is: {}".format(dict))
    print("statistics is {}".format(statistics))
    # Double_Letter test
    # dict = Double_Letter(c, dict, statistics)
    '''
    # match with L
    for i in range(len(L)):
        temp = Word_Judge(c, L[i])
        for j in range(len(L[i])):
            dict = ChangeDict(dict, temp[L[i][j]], L[i][j])
    # output possible plaintext
    plaintext, word_list = de_Trans(c, dict), []
    '''
    fp = open("dictionary.txt", mode="r")
    for item in fp.readlines():
        word_list.append(item.strip("\n"))
    '''
    print(">>>ciphertext: " + c)
    print(">>>plaintext : " + "".join(plaintext))
    print("<input \"quit\" to end this program>")
    p, d = Userfix(plaintext, dict)
    return ("".join(p), d)


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
    # print(dict)
    statistics = sorted(dict, key=dict.__getitem__, reverse=True)
    # create a dict to record letter-mapping
    for i in range(26):
        dict[statistics[i]] = frequency[i]
    # print("Single-letter: {}".format(dict))
    return (dict, statistics, frequency)


def Double_Letter(c, dict, stat):
    frequency = ['th', 'he', 'in', 'er', 'an', 're',
                 'ed', 'on', 'es', 'st', 'en', 'at',
                 'to', 'nt', 'ha', 'nd', 'ou', 'ea',
                 'ng', 'as', 'or', 'ti', 'is', 'et',
                 'it', 'ar', 'te', 'se', 'hi', 'of']
    statistics, d_dict = {}, {}
    string = c.split(" ")
    for i in range(len(string)):
        for j in range(len(string[i]) - 1):
            temp = string[i][j] + string[i][j + 1]
            if temp not in statistics:
                statistics[temp] = 1
            else:
                statistics[temp] += 1
    print(statistics)
    statistics = sorted(statistics, key=statistics.__getitem__, reverse=True)
    print(statistics)
    for i in range(26):
        d_dict[chr(ord("a") + i)] = 0
    for i in range(len(frequency)):
        # 对单字母频率后13个不常用字母进行双字母频率的字典修改
        if (d_dict[frequency[i][0]] == 0) and (statistics[i][0] not in stat[13:]):
            dict = ChangeDict(dict, statistics[i][0], frequency[i][0])
            d_dict[frequency[i][0]] = 1
        if (d_dict[frequency[i][1]] == 1) and (statistics[i][0] not in stat[13:]):
            dict = ChangeDict(dict, statistics[i][1], frequency[i][1])
        d_dict[frequency[i][0]] = 1
    return dict


def Word_Judge(c, word):
    c = c.replace(" ", "")
    stat_dict, result = {}, {}
    for i in range(0, len(c) - len(word) + 1):
        temp = c[i:i + len(word)]
        if temp not in stat_dict:
            stat_dict[temp] = 1
        else:
            stat_dict[temp] += 1
    stat_dict = sorted(stat_dict, key=stat_dict.__getitem__, reverse=True)
    for i in range(len(word)):
        result[word[i]] = stat_dict[0][i]
    return result


def Userfix(plaintext, dict):
    while (1):
        readin = input("   key-value to change: ")
        if (readin != "quit"):
            key, value = readin.split(":")
        else:
            break
        plaintext = []
        dict = ChangeDict(dict, key, value)
        for i in range(len(c)):
            if c[i].isalpha() == False:
                plaintext.append(' ')
            else:
                plaintext.append(dict[c[i]])
        print(">>>ciphertext: " + c)
        print(">>>plaintext : " + "".join(plaintext))
    return (plaintext, dict)


def de_Trans(c, dict):
    plaintext = []
    for i in range(len(c)):
        if c[i].isalpha() == False:
            plaintext.append(c[i])
        else:
            plaintext.append(dict[c[i]])
    return plaintext


if __name__ == "__main__":
    c = input("input ciphertext: ").lower()
    plaintext, dict = LFA(c)
    print("plaintext is: {}".format(plaintext))
    print("dict is: {}".format(dict))
    os.system("pause")
