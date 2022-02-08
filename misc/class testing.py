from itertools import count


class parent:
    id_iter = count()

    def __init__(self):
        self.id = next(self.id_iter)


class subclass(parent):
    id_iter = count()

    def __init__(self):
        super().__init__()


p = [parent() for _ in range(8)]
for t in p:
    print(t.id)

print()

s = [subclass() for _ in range(8)]
for t in s:
    print(t.id)
