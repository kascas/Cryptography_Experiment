import string
from bloom import *
import re
from Crypto.Cipher import AES
from aes import *


def _stat_word(filename):
    wordList, bloom = [], {}
    with open(filename, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip('\n').lower()
            # extract english chars
            enre = re.compile(r'[\u0061-\u007a]|[\u0020-\u002f]|[\u005b-\u0060]|[\u003a-\u0040]|[\u007b-\u007e]')
            # extract chinese chars
            cnre = re.compile(r'[\u4e00-\u9fa5]')
            en = ''.join(enre.findall(line.lower()))
            cn = ''.join(cnre.findall(line.lower()))
            # add english chars into bf
            for word in en.split():
                tmp = word.strip(string.punctuation)
                if tmp != '':
                    wordList.append(tmp)
            # add chinese chars into bf
            for i in range(len(cn)):
                wordList.append(cn[i])
    # delete repetitive words
    result = sorted(set(wordList), key=wordList.index)
    if len(result) < 1000:
        entries = 1000
    else:
        entries = len(result)
    bloom_init(bloom, entries, 1 / entries)
    # put words into bf
    key, iv = getKey()
    cipher = AES.new(key, AES.MODE_ECB)
    for i in range(len(result)):
        List = padding(result[i].encode('utf-8'))
        for j in List:
            bloom_add(bloom, cipher.encrypt(j))
    bloom_write(bloom, './bloom.json')
    return


def _word_extract(line):
    wordList = []
    line = line.strip('\n').lower()
    # extract english chars
    enre = re.compile(r'[\u0061-\u007a]|[\u0020-\u002f]|[\u005b-\u0060]|[\u003a-\u0040]|[\u007b-\u007e]')
    # extract chinese chars
    cnre = re.compile(r'[\u4e00-\u9fa5]')
    en = ''.join(enre.findall(line.lower()))
    cn = ''.join(cnre.findall(line.lower()))
    # add english chars into bf
    for word in en.split():
        tmp = word.strip(string.punctuation)
        if tmp != '':
            wordList.append(tmp)
    # add chinese chars into bf
    for i in range(len(cn)):
        wordList.append(cn[i])
    result = sorted(set(wordList), key=wordList.index)
    return result


if __name__ == "__main__":
    List = _stat_word('./File/a.txt')
    bloom = bloom_read('./bloom.json')
    while True:
        print(bloom_check(bloom, input('word: ')))
