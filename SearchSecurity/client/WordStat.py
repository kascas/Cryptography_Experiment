import string
from bloom import *
import re


def _stat_word(filename):
    wordList, bloom = [], {}
    with open(filename, 'r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip('\n').lower()
            enre = re.compile(r'[\u0061-\u007a]|[\u0020-\u002f]|[\u005b-\u0060]|[\u003a-\u0040]|[\u007b-\u007e]')
            cnre = re.compile(r'[\u4e00-\u9fa5]')
            en = ''.join(enre.findall(line.lower()))
            cn = ''.join(cnre.findall(line.lower()))
            for word in en.split():
                tmp = word.strip(string.punctuation)
                if tmp != '':
                    wordList.append(tmp)
            for i in range(len(cn)):
                wordList.append(cn[i])
    result = sorted(set(wordList), key=wordList.index)
    print(result)
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
