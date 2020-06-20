from ctypes import *


def _bloom_init(call, entries, error):
    call.bloom_init(c_int(entries), c_double(error))
    return


def _bloom_add(call, word):
    byte = bytes(word, 'utf-8')
    call.bloom_add(byte, len(byte))
    return


def _bloom_check(call, word):
    byte = bytes(word, 'utf-8')
    result = call.bloom_check(byte, len(byte))
    return result


def _bloom_print(call):
    call.bloom_print()
    return


def _bloom_read(call, filename):
    call.bloom_read(filename)
    return


def _bloom_write(call, filename):
    call.bloom_write(filename)
    return


if __name__ == "__main__":
    call = cdll.LoadLibrary('./bloom.dll')
    _bloom_init(call, 1000, 0.001)
    _bloom_add(call, 'hello')

    _bloom_write(call, './bloom.bf'.encode('utf-8'))
    _bloom_read(call, './bloom.bf'.encode('utf-8'))

    print(_bloom_check(call, 'world'))
    print(_bloom_check(call, 'hello'))
    print(_bloom_check(call, 'baidu'))
    _bloom_print(call)
