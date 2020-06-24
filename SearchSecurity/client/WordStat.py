import string
from bloom import *


def _stat_word(filename):
    wordList, bloom = [], {}
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
    bloom_init(bloom, entries, 1 / entries)
    for i in range(len(result)):
        bloom_add(bloom, result[i])
    bloom_write(bloom, './bloom.json')
    return


if __name__ == "__main__":
    List = _stat_word('./File/a.txt')
    bloom = bloom_read('./bloom.json')
    while True:
        print(bloom_check(bloom, input('word: ')))
