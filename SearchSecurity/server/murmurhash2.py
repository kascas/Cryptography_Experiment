def murmurhash2(key, length, seed):
    m, r, h, data, i = 0x5bd1e995, 24, seed ^ length, key[:], 0
    while (length >= 4):
        k = ((ord(data[i + 3]) << 24) + (ord(data[i + 2]) << 16) + \
             (ord(data[i + 1]) << 8) + ord(data[i])) & 0xffffffff
        k = (k * m) & 0xffffffff
        k ^= k >> r
        k = (k * m) & 0xffffffff

        h = (h * m) & 0xffffffff
        h ^= k

        length -= 4
        i += 4
    if length == 3:
        h ^= ord(data[i + 2]) << 16
        h ^= ord(data[i + 1]) << 8
        h ^= ord(data[i])
        h = (h * m) & 0xffffffff
    elif length == 2:
        h ^= ord(data[i + 1]) << 8
        h ^= ord(data[i])
        h = (h * m) & 0xffffffff
    elif length == 1:
        h ^= ord(data[i])
        h = (h * m) & 0xffffffff

    h ^= h >> 13
    h = (h * m) & 0xffffffff
    h ^= h >> 15
    return h


if __name__ == "__main__":
    print(murmurhash2('hello', len('hello'), 0))
