from timeit import timeit


def timer(n):
    return n


s = []
try:
    while True:
        t = timeit("timer(21021)", setup="from timing import timer")
        s.append(t)
        print(t)

except KeyboardInterrupt:
    print(f"Average:{sum(s) / len(s)}")
