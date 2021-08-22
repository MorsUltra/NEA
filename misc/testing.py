import pprint

perm_index = 21021
factoradic = ""
variable_base = 0
while perm_index:
    variable_base += 1
    remainder = perm_index % variable_base
    perm_index //= variable_base
    factoradic += str(remainder)

perm = [0] * 8
corner_index = list(range(0, 8))
for x in range(len(corner_index) - 1, -1, -1):
    perm[x] = corner_index.pop(x - int(factoradic[x]))

print(perm)