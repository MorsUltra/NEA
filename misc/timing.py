from functools import reduce
from timeit import timeit
from math import comb as CNK
from itertools import count as counter


def timer(index: int):
    count = 3
    ep = [False] * 12

    for i in range(11, -1, -1):
        if count < 0:
            break

        v = CNK(i, count)

        if index < v:
            ep[i] = 8 + count
            count -= 1
        else:
            index -= v

    c = counter(0)
    for i, edge in enumerate(ep):
        if not edge:
            ep[i] = next(c)

    return ep


s = []
try:
    count = 0
    while True:
        t = timeit("timer(193)", globals=globals())
        s.append(t)
        print(t)
        count += 1
        if count % 10 == 0:
            print(f"Average: {sum(s) / len(s)}")

except KeyboardInterrupt:
    print(f"Average:{sum(s) / len(s)}")
