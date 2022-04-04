from timeit import timeit


def timer(ep):
    index = 0
    for p in range(11, 8, -1):
        higher = 0
        for edge in ep[8:p]:
            if edge > ep[p]:
                higher += 1

        index = (index + higher) * (p-8)

    return index


s = []
try:
    count = 0
    while True:
        t = timeit("timer([0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 8, 11])", globals=globals())
        s.append(t)
        print(t)
        count += 1
        if count % 10 == 0:
            print(f"Average: {sum(s) / len(s)}")

except KeyboardInterrupt:
    print(f"Average:{sum(s) / len(s)}")
