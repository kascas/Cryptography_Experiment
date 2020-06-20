import string


def _stat(filename):
    wordList = []
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            line = line.strip('\n')
            line = line.strip(string.digits)
            line = line.strip(string.punctuation)
            line = line.rstrip(string.punctuation)
            for word in line.split():
                wordList.append(word)
    return wordList


if __name__ == "__main__":
    List = _stat('./File/4.txt')
    print(List)
    print(len(List))
