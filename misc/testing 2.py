def Pcorner_coordsd1(index):
    corners = list(range(8))
    cp = [-1] * 8
    coeffs = [0] * 7

    for i in range(2, 9):
        coeffs[i - 2] = index % i
        index //= i

    print(coeffs)
    for i in range(7, 0, -1):
        cp[i] = corners.pop(i - coeffs[i - 1])

    cp[0] = corners[0]

    return cp

def Pcorner_coordst1(index):
    corners = list(range(7, -1, -1))
    cp = [-1] * 8
    coeffs = []

    for i in range(2, 9):
        coeffs.insert(0, index % i)
        index //= i

    print(coeffs)
    for i in range(7):
        cp[7-i] = corners.pop(coeffs[i])

    cp[0] = corners[0]

    return cp


def Pcorner_coords1(cp):  # working
    index = 0
    # Fairly confident this is working. Not the problem
    for p in range(7, 0, -1):
        higher = 0
        for corner in cp[:p]:
            if corner > cp[p]:
                higher += 1

        index = (index + higher) * p

    return index


print(Pcorner_coordsd1(3651))
print(Pcorner_coordst1(3651))

# for x in range(40319):
#     if Pcorner_coordsd1(x) != Pcorner_coordst1(x):
#         print(f"Error at {x}")
