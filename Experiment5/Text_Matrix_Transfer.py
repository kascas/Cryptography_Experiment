def Text_into_Matrix(s):
    '''
    transfer text into byte-matrix
    :param s:
    :return: a matrix
    '''
    temp, matrix = s.to_bytes(16, 'big'), [[] for i in range(4)]
    for i in range(16):
        matrix[i % 4].append(temp[i])
    return matrix


def Matrix_into_Text(state):
    result = 0
    for i in range(4):
        for j in range(4):
            result <<= 8
            result += state[j][i]
    return result
