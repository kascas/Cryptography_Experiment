import string
import BloomFilter as BF
from ctypes import *


def _stat_word(call, filename):
    wordList = []
    with open(filename, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip('\n').lower()
            # line = line.translate(str.maketrans(string.punctuation, ' ' * 32))
            # line = line.translate(str.maketrans(string.digits, ' ' * 10))
            for word in line.split():
                wordList.append(word.strip(string.punctuation))
    result = sorted(set(wordList), key=wordList.index)
    if len(result) < 1000:
        entries = 1000
    else:
        entries = len(result)
    BF._bloom_init(call, entries, 1 / entries)
    for i in range(len(result)):
        BF._bloom_add(call, result[i])
    BF._bloom_write(call, './bloom.bf'.encode('utf-8'))
    BF._bloom_free(call)
    return


if __name__ == "__main__":
    call = cdll.LoadLibrary('./bloom.dll')
    List = _stat_word(call, './File/test1.txt')
    BF._bloom_print(call)
    while True:
        print(BF._bloom_check(call, input('word: ')))
