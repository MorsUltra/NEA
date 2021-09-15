# Rubiks cube solver 

## The two phase algorithm

Each cube can be represented by a series of coordinates that each describe an attribute of that cube. For instance, the orientation of the corners and the edges, or the position of some pieces. 

Certain turns of the cube's faces do not effect some of these attributes. For instance, double turns of any face but the cube's relative top and bottom will not change the orientation of the corners or edges.

With this information, it's possible to split the cube's various states into different groups or *co-sets* that are achievable whilst a constraint has been placed on the moves you can apply to the cube.

The first group, you only consider the orientation of the corners and edges, as well as the position of the *UD-slice* (UD-slice refers to the edges bounded by the U and D faces) edges (we do not consider how these edges are orientated or positioned, just which edge spaces are occupied by these middle edges).

This effectifly limits both the quantity of data you have to keep tract of when manipulating the cube (for instance, the position of the pieces), and the distance you have to search through to reach the indentity element of this group - a cube where the edges and corners are orientated correctly, and where the UD-slice edges are somewhere in the UD-slice.

The aforementined coorinates are represented in various ways that best suite what they represent:

### The corner orientation coordinate
A corner can be orientated one of three ways which therefore warrents a ternary number system as the most fitting method of representing each corner.

**0** implies that the corner is not rotated from its default state (as defined in some basic setup)
**1** that the corner has been twisted once clockwise
**2** that the conner has been twisted twice clockwise - this is synonomous with an anti-clockwise rotation.

It follows that we can store the orientation of each corner as `ori = ori mod 3` to simplify things. 

To again minimise the size of the numbers required to elements of the group, we can exclude the last corner form our ternary number as for a cube to be reachable throught normal means the sum of all the orientations of the coners most satisfy `sum mod 3 = 0`. Intuitively this means that there is not a singular corner twisted individually, as a turn of the face will always impact 4 corners.

The following function reduces the orientation of the corners `[0, 2, 2, 0, 2, 2, 1, 0]` to a ternary number `673` with range `3 pow 7 - 1 = 2186 <---> 0`:
```
@property
def Ocorner_coords(self):
    co = reduce(lambda variable_base, total: 3 * variable_base + total, self.co[:7])

    return co
```

The following does the opposite, taking the index of the element in the corner orientation co-set of the cube group and computing the orientation of the corners:
```
@Ocorner_coords.setter
def Ocorner_coords(self, index):
    parity = 0
    self.co = [-1] * 8
    for _ in range(6, -1, -1):
        parity += index % 3
        self.co[_] = index % 3
        index //= 3

    parity %= 3
    parity = self.Ocorner_parity_value[parity]
    self.co[-1] = parity
```

### The edge orientation coordinate
The orientation of the edges can be defined in much the same way - a binary system is used where *0* implies an unflipped edge and *1* the contrary.

Again, a similar method can be used to minimise the size of said number: the orientation of the final edge is omitted and calculated such that `sum mod 2 = 0`.
```
@property
def Oedge_coords(self):  # working
    eo = reduce(lambda variable_base, total: 2 * variable_base + total, self.eo[:11])

    return eo
```
The index of the element has range `2 pow 11 - 1 = 2047 <---> 0` and the following function reverses it in a similar manner to the corners:
```
@Oedge_coords.setter
def Oedge_coords(self, index):
    parity = 0
    self.eo = [-1] * 12
    for _ in range(10, -1, -1):
        parity += index % 2
        self.eo[_] = index % 2
        index //= 2

    self.eo[-1] = parity % 2
```

### The UD-slice coordinate
e

e

e


e


e


e


e



## Facelet level
The cube must first be defined by a 1d string of characters that represent the colours of each of the 54 faceltes present on the cube.

They are numbered from **top-down from left to right**, in the order of *axis* as defined here:

```
class colours(IntEnum):
    U = 0
    R = 1
    L = 2
    F = 3
    B = 4
    D = 5
```
Note that the *IntEnum* module is used to allow the program to allow for the axis to be treated as integers, as well as providing some functional utility for debugging later as it's much easier to comprehend the "U" axis as opposed to the integer 0.

The facelet level definition is a string of length 54 composed of the characters featured in `colours`. It's worth noting that whilst the cube itself is relative, the axes are constant.

A solved cube in facelet defintion will look like this: 
```
UUUUUUUUURRRRRRRRRLLLLLLLLLFFFFFFFFFBBBBBBBBBDDDDDDDDD
```
This is the *identity* defintion