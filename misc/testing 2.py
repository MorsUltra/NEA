from math import factorial


def Pcorner_coordss(index: int):
    """
    Algorithm to set the permutation of corners of the coordinate between 0-40319.

    @param index: coordinate of corner permutation.
    """
    cp = [0, 0, 0, 0, 0, 0, 0, 0]
    # Create an empty list of corners.
    corners = [7, 6, 5, 4, 3, 2, 1, 0]
    # Create empty factoradic number.
    factoradic = []

    # Increase the radix with each of the 7 steps.
    for mixed_radix in range(2, 8):
        # Add the remainder to the factoradic to record how many (mixed_radix!) are a part of the number.
        factoradic.append(index % mixed_radix)
        # Remove (mixed_radix!) as a factor from index.
        index //= mixed_radix

    # Add the final remainder to the factoradic.
    factoradic.append(index)

    # For each coefficient in the factoradic
    for i in range(7, 0, -1):
        # Pop the relevant corner from the list per the factoradic number.
        cp[i] = corners.pop(factoradic[i - 1])

    # Append the final corner.
    cp[0] = corners[0]
    return cp


def Pcorner_coordsd(cp):  # working
    index = 0
    # Fairly confident this is working. Not the problem
    for p in range(7, 0, -1):
        higher = 0
        for corner in cp[:p]:
            if corner > cp[p]:
                higher += 1

        index = (index + higher) * p

    return index


def Pcorner_coordst(cp):  # working
    return sum(factorial(i) * v for i, v in enumerate(cp))


print(Pcorner_coordsd([1, 3, 4, 2, 5, 7, 0, 6]))
print(Pcorner_coordst([0, 1, 2, 3, 4, 5, 6, 7]))

for x in range(40320):
    p = Pcorner_coordss(x)
    if Pcorner_coordsd(p) != Pcorner_coordst(p):
        print(f"Error at {x}")
