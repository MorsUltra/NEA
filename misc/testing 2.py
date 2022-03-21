def Ocorner_coords(index: int) -> list[int]:
    # Average:0.7582400450133718

    Ocorner_parity_value = [0, 2, 1]

    parity = 0
    co = [-1] * 8
    for i in range(6, -1, -1):
        parity += index % 3
        co[i] = index % 3
        index //= 3

    parity %= 3
    parity = Ocorner_parity_value[parity]
    co[-1] = parity
    return co


def Ocorner_coords2(index: int) -> list[int]:
    # Average: 0.7458249650080688

    Ocorner_parity_value = [0, 2, 1]

    parity = 0
    co = [-1] * 8
    for i in range(6, -1, -1):
        remainder = index % 3
        parity += remainder
        co[i] = remainder
        index //= 3

    parity %= 3
    parity = Ocorner_parity_value[parity]
    co[-1] = parity
    return co


def Ocorner_coords3(index: int) -> list[int]:
    # Average:0.8358729499974288

    Ocorner_parity_value = [0, 2, 1]

    parity = 0
    co = [-1] * 8
    for i in range(6, -1, -1):
        index, remainder = divmod(index, 3)
        parity += remainder
        co[i] = remainder

    parity %= 3
    parity = Ocorner_parity_value[parity]
    co[-1] = parity
    return co


def Ocorner_coords4(index: int) -> list[int]:
    # Average:0.6830658300139476

    Ocorner_parity_value = [0, 2, 1]

    co = [0] * 8
    for i in range(6, -1, -1):
        co[i] = index % 3
        index //= 3

    co[7] = Ocorner_parity_value[sum(co) % 3]
    return co


for x in range(2188):
    if Ocorner_coords(x) != Ocorner_coords4(x):
        print(f"Error at {x}")
