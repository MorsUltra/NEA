class obj:
    c = 2

    def __init__(self):
        self.i = self.c
        obj.c += 1


list = [obj() for x in range(10)]

for x in list:
    print(x.i)

for i, o in enumerate(list):
    o.i += 1

print("\n\n\n\n")

for x in list:
    print(x.i)
