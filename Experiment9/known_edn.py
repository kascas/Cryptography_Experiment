import os


def phi_n(e, d, n):
    '''
    it is known that e*d-1=m*phi_n
    phi_n=p*q-(p+q)+1
    p and q are very large, but (p+q)/p*q could be very small
    thus, m=(e*d-1)/phi_n exist near to (e*d-1)/n
    :param e:
    :param d:
    :param n:
    :return:
    '''
    mul = e * d - 1
    base = mul // n
    min, max = int(base * 0.9), int(base * 1.1)
    prob = []
    for i in range(min, max):
        if mul % i == 0:
            prob.append(mul // i)
    return prob


def factor(e, d, n):
    '''
    in this function, (p+q),(p*q) are known.
    then we can compute (p-q) according to (p-q)=sqrt((p+q)^2-4*p*q)
    finally we can compute p and q according to (p+q) and (p-q)
    according to (p+q) and (p-q) compute (p,q)
    :param e: public key
    :param d: private key
    :param n: mod num
    :return: the factorization of n
    '''
    pn_list, pn = phi_n(e, d, n), 0
    result = []
    for i in range(len(pn_list)):
        p_q_plus = n - pn_list[i] + 1
        p_q_square_plus = p_q_plus ** 2
        p_q_square_minus = p_q_square_plus - 4 * n
        p_q_minus = sqrt(p_q_square_minus)
        p, q = (p_q_plus + p_q_minus) // 2, (p_q_plus - p_q_minus) // 2
        result.append((p, q))
    return result


def sqrt(n):
    '''
    use BinarySearch to find the root
    :param n: n
    :return: sqrt(n)
    '''
    low = 0
    height = n - 1
    while low < height:
        mid = (low + height) // 2 + 1
        if mid ** 2 < n:
            low = mid + 1
        elif mid ** 2 > n:
            height = mid - 1
        else:
            return mid
    return -1


if __name__ == "__main__":
    n = 21378032245774894186324720788457768851857953294637267751313371903474996018902810092972224806315945430514626988743400353365786674788848003569698586194388463460699531620948408197942261177369324808332585418351947368544183614904162658914539989430070735676083960582943505227316151479174351490943931346982185481068889458087344890907035731467000101100009111593455801160870652558847164438348031498067369123608755518383163346962891967964682970251625764813457371461595048927486942272152822570449609158417324070867001419543608370026546341531367233199832189762919523227554947408242727690461831545997600374969434706782376320559561
    e = 65537
    d = 13085102850405329895940153649208766646679432053055210927814587187939575969334380946175257120108607885616731724467899991987963542311668962802613624160423864736904359544115910805381019345850330276964971412664144174157825068713331109139842487999112829255389047329358923488846912437792391102853729375052922599258215311601018992134762683570752403675370812499995354701024990414541327012769030147878934713424171374951602988478984432403148854042370903764361797455965930292322795814453835335323397068237664481359506461188857661605832041501219728374514303209642746672993156029099655958158717907546664548938973389857200804582177
    p, q = factor(e, d, n)[0]
    print('p: {}'.format(p))
    print('q: {}'.format(q))
    print(p * q - n)
    os.system("pause")
