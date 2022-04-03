from timeit import timeit


def timer(index):
    cp = [-1] * 8
    factoradic = [0] * 7

    for i in range(2, 9):
        factoradic[i - 2] = index % i
        index //= i

    corners = list(range(8))
    for i in range(7, 0, -1):
        cp[i] = corners.pop(i - factoradic[i - 1])

    cp[0] = corners[0]

    return cp


s = []
try:
    count = 0
    while True:
        t = timeit("timer(40319)", globals=globals())
        s.append(t)
        print(t)
        count += 1
        if count % 10 == 0:
            print(f"Average: {sum(s) / len(s)}")

except KeyboardInterrupt:
    print(f"Average:{sum(s) / len(s)}")
