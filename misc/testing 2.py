from math import comb as CNK
from itertools import count as counter


def Pcorner_coords(index):
    corners = list(range(8))
    cp = [-1] * 8
    coeffs = [0] * 7

    for i in range(2, 9):
        coeffs[i - 2] = index % i
        index //= i

    print(coeffs)

    for i in range(7, 0, -1):
        cp[i] = corners.pop(i - coeffs[i - 1])

    cp[0] = corners[0]

    return cp

def Pcorner_coords1(cp):  # working
    index = 0
    # Fairly confident this is working. Not the problem
    for p in range(7, 0, -1):
        higher = 0
        for corner in cp[:p]:
            if corner > cp[p]:
                higher += 1

        index = (index + higher) * p

    return index

print(Pcorner_coords(40319))
