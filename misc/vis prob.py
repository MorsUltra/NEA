import string
import math
import matplotlib.pyplot as plt
import random

k = 1
letters = dict(zip(string.ascii_lowercase, range(1, 26)))
letter = "a"
lettersubnumber = letters[letter]


def reorder(list, start_index):
    start_index -= 1
    for i in range(start_index + 1, len(list)):
        yield list[i]
    for i in range(0, start_index):
        yield list[i]


def circular(input):
    while True:
        for i in input:
            yield i


def depth_gen(data, indicies):
    data = list(data)
    new = []
    for _ in range(len(data)):
        new.append(data.pop(next(indicies)))

    newsubindex = []
    for i, letter in enumerate(new):
        newsubindex.append([letter, (i // 2) + 1])
    return newsubindex


def Panalysis(k):
    y = []
    for i in range(0, 26):
        y.append(math.pow(math.e, (-i / k)))
    plt.figure(1)
    plt.subplot(111)
    plt.plot(range(0, 26), y)
    plt.show()


def P(depth, k):
    PsubGeneration = math.pow(math.e, (-depth / k))
    return PsubGeneration


letters = [i for i in string.ascii_lowercase]
indicies = circular([0, -1])
data = reorder(letters, lettersubnumber)
new = depth_gen(data, indicies)
for node in new:
    node[1] = P(node[1], k)

Panalysis(k)
for node in new:
    print(node[0], node[1] * 100)

# TODO: Use new function to guarantee binding to adjacent to one another
# TODO: Use UUID to generate many new nodes and pass then through the graph algorithm mentioned above

network = {letter: []}
print("\n\n\n\n\n")
for node, probability in new:  #
    rand = random.randint(0, 10)
    print(rand, probability * 100)
    if rand <= probability * 100:
        network[letter].append(node)

print(network)