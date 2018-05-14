cache = {}
def P(n, m, u):
    key = (n, m, u)
    if key in cache.keys():
        return cache[key]

    if u < 0:
        value = 0
    elif n == 0 and u != 0:
        value = 0
    elif m == 0 and u != 0:
        value = 0
    elif n == 0 and u == 0:
        value = 1
    elif m == 0 and u == 0:
        value = 1
    else:
        value = ((n/(n+m)) * P(n - 1.0, m, u - m)) + ((m/(n+m)) * P(n, m - 1.0, u))
    cache[key] = value
    return value


def post_P(n, m, u):
    sum = 0
    for i in range(0, u+1):
        sum += P(n, m, i)
    return sum

def u_cirt(n, m, alpha):
    sum = 0
    u_max = -1
    while True:
        sum += P(n, m, u_max + 1)
        if sum > alpha:
            break
        else:
            u_max += 1
    return u_max

if __name__ == '__main__':
    from prettytable import PrettyTable
    x = PrettyTable()

    m_max = 20
    n_max = 20
    alpha = 0.05

    print('One-tailed U test crit value table')
    print('alpha = %f' % alpha)
    fs = ["n\m"]
    for m in range(1, m_max + 1):
        fs.append(str(m))

    x.field_names = fs

    for n in range(1, n_max + 1):
        row = [str(n)]
        for m in range(1, m_max + 1):
            u_c = u_cirt(n, m, alpha)
            if (u_c == -1):
                row.append(' ')
            else:
                row.append('%d' % u_c)
        x.add_row(row)

    print(x)