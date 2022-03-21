from functools import reduce
from timeit import timeit


def timer(index: int):

    Ocorner_parity_value = [0, 2, 1]
    co = [0] * 8
    # Loop through the 7 most significant bits, leaving the last to be implied.
    for i in range(6, -1, -1):
        # Collect the bit at index i which has significance 3^i; the remainder when divided by 3^i.
        co[i] = index % 3
        # Move to the next bit.
        index //= 3

    # Set the least significant bit by finding the bit required to make the sum a multiple of 3.
    co[7] = Ocorner_parity_value[sum(co) % 3]
    return co


s = []
try:
    count = 0
    while True:
        t = timeit("timer(2023)", setup="from timing import timer")
        s.append(t)
        print(t)
        count += 1
        if count % 10 == 0:
            print(f"Average:{sum(s) / len(s)}")

except KeyboardInterrupt:
    print(f"Average:{sum(s) / len(s)}")
