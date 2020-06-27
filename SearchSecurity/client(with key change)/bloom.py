from murmurhash2 import *
from math import *
from json import *

'''
bloom = {
    'entries': 0,
    'error': 0.0,
    'bits': 0,
    'bytes': 0,
    'hashes': 0,
    'bpe': 0.0,
    'bf': [],
    'ready': 0
}
'''


def test_bit_set_bit(buf, x, set_bit):
    byte = x >> 3
    c = buf[byte]
    mask = (1 << (x % 8)) & 0xffffffff
    if c & mask:
        return 1
    else:
        if set_bit:
            buf[byte] = c | mask
        return 0


def bloom_check_add(bloom, buffer, add):
    if bloom['ready'] == 0:
        print('bloom not initialized!\n')
        return -1
    hits = 0
    a = murmurhash2(buffer, len(buffer), 0x9747b28c)
    b = murmurhash2(buffer, len(buffer), a)
    for i in range(bloom['hashes']):
        x = ((a + i * b) & 0xffffffff) % bloom['bits']
        if test_bit_set_bit(bloom['bf'], x, add):
            hits += 1
        elif not add:
            return 0
    if hits == bloom['hashes']:
        return 1
    return 0


def bloom_init(bloom, entries, error):
    bloom['ready'] = 0
    if entries < 1000 or error == 0:
        return 1
    bloom['entries'] = entries
    bloom['error'] = error
    num = log(bloom['error'])
    denom = 0.480453013918201
    bloom['bpe'] = -1 * (num / denom)
    dentries = entries
    bloom['bits'] = int(dentries * bloom['bpe'])
    bloom['bytes'] = ceil(bloom['bits'] / 8)
    bloom['hashes'] = ceil(0.693147180559945 * bloom['bpe'])
    bloom['bf'] = [0 for i in range(bloom['bytes'])]
    bloom['ready'] = 1
    return


def bloom_check(bloom, buffer):
    return bloom_check_add(bloom, buffer, 0)


def bloom_add(bloom, buffer):
    return bloom_check_add(bloom, buffer, 1)


def bloom_print(bloom):
    print(bloom)
    return


def bloom_reset(bloom):
    bloom['entries'] = 0
    bloom['error'] = 0.0
    bloom['bits'] = 0
    bloom['bytes'] = 0
    bloom['hashes'] = 0
    bloom['bpe'] = 0.0
    bloom['bf'] = []
    bloom['ready'] = 0
    return


def bloom_write(bloom, filename):
    with open(filename, 'w') as fp:
        js = dumps(bloom)
        fp.write(js)
    return


def bloom_read(filename):
    fp = open(filename, encoding='utf-8')
    bloom = load(fp)
    return bloom


if __name__ == "__main__":
    bloom = {}
    bloom_init(bloom, 1000, 0.001)
    for i in range(5):
        word = input('word: ')
        bloom_add(bloom, word)
    bloom_print(bloom)

    bloom_write(bloom, './tmp.json')
    bloom_reset(bloom)
    bloom = bloom_read('./tmp.json')

    while True:
        word = input('check: ')
        print(bloom_check(bloom, word))
