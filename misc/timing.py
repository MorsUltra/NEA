from functools import reduce
from timeit import timeit
from math import comb as CNK
from itertools import count as counter


def timer(index):
    corners = list(range(8))
    cp = [-1] * 8
    coeffs = [0] * 7

    for i in range(2, 9):
        coeffs[i - 2] = index % i
        index //= i

    for i in range(7, 0, -1):
        cp[i] = corners.pop(i - coeffs[i - 1])

    cp[0] = corners[0]

    return cp


s = []
try:
    count = 0
    while True:
        t = timeit("timer(21312)", globals=globals())
        s.append(t)
        print(t)
        count += 1
        if count % 10 == 0:
            print(f"Average: {sum(s) / len(s)}")

except KeyboardInterrupt:
    print(f"Average:{sum(s) / len(s)}")
