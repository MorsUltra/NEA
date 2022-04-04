def P4edge_coordst(index: int):
    """
    Function to set the permutation of the UD-slice edge permutation based off of the coordinate between 0 --> 23
    (4! - 1).

    :param index: the coordinate of the UD-slice edge permutation.
    """

    # Create an empty list of UD-slice edges.
    ep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    edges = [11, 10, 9, 8]
    # Create empty factoradic
    factoradic = []

    # Increase the radix with each of the 3 steps.
    for mixed_radix in range(2, 5):
        # Add the remainder to the factoradic to record how many (mixed_radix!) are a part of the number.
        factoradic.append(index % mixed_radix)
        # Remove (mixed_radix!) as a factor from index.
        index //= mixed_radix

    for i in range(3, 0, -1):
        ep[8 + i] = edges.pop(factoradic[i - 1])

    ep[8] = edges[0]

    return ep


def P4edge_coordsd(index):
    ep = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    ep[8:] = [-1] * 4

    corners = list(range(8, 12))
    coeffs = [0] * 3
    for i in range(2, 5):
        coeffs[i - 2] = index % i
        index //= i

    for i in range(3, 0, -1):
        ep[8 + i] = corners.pop(i - coeffs[i - 1])

    ep[8] = corners[0]

    return ep


# from itertools import permutations
#
# for x in permutations([8, 9, 10, 11]):
#     p = [0, 1, 2, 3, 4, 5, 6, 7] + list(x)
#     if P4edge_coordst(p) != P4edge_coordst(p):
#         print("Error")

for x in range(23):
    if P4edge_coordsd(x) != P4edge_coordst(x):
        print("Error")
