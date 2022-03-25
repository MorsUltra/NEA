from math import comb as CNK
from itertools import count as counter

def POSud_slice_coords(index):
    # Average: 1.9269003249995875
    count = 3
    ep = [False] * 12

    for i in range(11, -1, -1):
        if count < 0:
            break

        v = CNK(i, count)

        if index < v:
            ep[i] = 8 + count
            count -= 1
        else:
            index -= v

    others = 0
    for i, edge in enumerate(ep):
        if not edge:
            ep[i] = others
            others += 1

    return ep

def POSud_slice_coords2(index):
    # Average:1.9269003249995875

    count = 4
    ep = [False] * 12
    others = 0

    for i in range(11, -1, -1):
        if not count:
            for unchecked in range(i+1):
                ep[unchecked] = others
                others += 1
            break

        v = CNK(i, count-1)

        if index < v:
            ep[i] = 7 + count
            count -= 1
            
        else:
            index -= v
            ep[i] = others
            others += 1

    return ep

print(POSud_slice_coords2(65))
print(POSud_slice_coords(65))


# for i in range(494):
#     if POSud_slice_coords(i) != POSud_slice_coords2(i):
#         print(i)
#         print(POSud_slice_coords2(i))
#         print(POSud_slice_coords(i))
