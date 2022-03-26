from functools import reduce
from timeit import timeit
from math import comb as CNK
from itertools import count as counter


def timer(ep):
    # Average: 1.082315575001121
    coordinate = 0
    pieces_remaining = 4

    for i in range(12):
        if not pieces_remaining:
            break

        if ep[i] >= 8:
            pieces_remaining -= 1
        else:
            coordinate += CNK(i, pieces_remaining - 1)

    return coordinate


s = []
try:
    count = 0
    while True:
        t = timeit("timer([7, 8, 6, 5, 4, 9, 3, 2, 10, 11, 1, 0])", globals=globals())
        s.append(t)
        print(t)
        count += 1
        if count % 10 == 0:
            print(f"Average: {sum(s) / len(s)}")

except KeyboardInterrupt:
    print(f"Average:{sum(s) / len(s)}")
