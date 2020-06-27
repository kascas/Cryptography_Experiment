def murmurhash2(key, length, seed):
    m, r, h, data, i = 0x5bd1e995, 24, seed ^ length, key[:], 0
    while (length >= 4):
        k = ((data[i + 3] << 24) + (data[i + 2] << 16) +
             (data[i + 1] << 8) + data[i]) & 0xffffffff
        k = (k * m) & 0xffffffff
        k ^= k >> r
        k = (k * m) & 0xffffffff

        h = (h * m) & 0xffffffff
        h ^= k

        length -= 4
        i += 4
    if length == 3:
        h ^= data[i + 2] << 16
        h ^= data[i + 1] << 8
        h ^= data[i]
        h = (h * m) & 0xffffffff
    elif length == 2:
        h ^= data[i + 1] << 8
        h ^= data[i]
        h = (h * m) & 0xffffffff
    elif length == 1:
        h ^= data[i]
        h = (h * m) & 0xffffffff

    h ^= h >> 13
    h = (h * m) & 0xffffffff
    h ^= h >> 15
    return h


if __name__ == "__main__":
    print(murmurhash2(b'hello', len(b'hello'), 0))
