def edge_parity(cp):
    parity = 0
    for q in range(11, 0, -1):
        for corner in cp[:q]:
            if corner > cp[q]:
                parity += 1
    return parity % 2

def edge_parity2(ep):
    parity = 0
    for q in range(11, 0, -1):
        for edge in ep[:q]:
            if edge > ep[q]:
                parity += 1

    return parity % 2

print(edge_parity([11,  7, 6, 5, 4, 10, 9, 8, 3, 2, 1, 0]))
print(edge_parity2([4, 3, 4, 0, 2, 3, 2, 0, 1, 5, 3, 5, 0], [2, 1, 2, 2, 2, 1, 2, 3, 2, 2, 1, 2, 1]))
