from functools import reduce
from timeit import timeit


def timer(co):
    co = reduce(lambda variable_base, total: 3 * variable_base + total, co[:7])
    return co

s = []
try:
    count = 0
    while True:
        t = timeit("timer([2, 2, 1, 0, 2, 2, 0, 2])", setup="from timing import timer")
        s.append(t)
        print(t)
        count += 1
        if count == 10:
            print(f"Average:{sum(s) / len(s)}")

except KeyboardInterrupt:
    print(f"Average:{sum(s) / len(s)}")
