# Rubiks cube solver 

## The two phase algorithm

Each cube can be represented by a series of coordinates that each describe an attribute of that cube. For instance, the orientation of the corners and the edges, or the position of some pieces. 

Certain turns of the cube's faces do not effect some of these attributes. For instance, double turns of any face but the cube's relative top and bottom will not change the orientation of the corners or edges.

With this information, it's possible to split the cube's various states into different groups or *co-sets* that are achievable whilst a constraint has been placed on the moves you can apply to the cube.

# Phase One
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
```python
@property
def Ocorner_coords(self):
    co = reduce(lambda variable_base, total: 3 * variable_base + total, self.co[:7])

    return co
```

The following does the opposite, taking the index of the element in the corner orientation co-set of the cube group and computing the orientation of the corners:
```python
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
```python
@property
def Oedge_coords(self):
    eo = reduce(lambda variable_base, total: 2 * variable_base + total, self.eo[:11])

    return eo
```
The index of the element has range `2 pow 11 - 1 = 2047 <---> 0` and the following function reverses it in a similar manner to the corners:
```python
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
The UD-slice coordinate uses a different encoding method altogether. At this point in the algorithm, the only nessessary data is **where** the UD-slice edges are, and not how they are rotated or where they are each positioned.

There are 4 edges, each of which can exist in one of 12 edges and it follow that the coordinate has range `2*11*10*9/4! - 1 = 494`.

The algoritm uses an array to represent each elelent in the UD-slice co-set much as the other methods of encoding expalined above, however assignes each of the elements in said array with a weight correspoding to their position `0, 1... 10, 11` and works from right to left: 

The number of UD-slice edges seen at the beginning of the algorithm is `4 - 1=3` such that `C(weight, seen_edges)` calculates the set of combinations of the remaining edges in the remaining spaces. This only works as all UD-slice edges are consiered homogenous here, so they are completely interchangable with one another. 

The algorihtm maps each element to an index on a 1 to 1 basis, and the identity elemnent is 0 here also, representing when the UD-slice edges are all stacked in final 4 positions in the array. Intuitively this means that they are all present in the UD-slice, but not necessarily in the right position nor orientation for the cube to be consiered solved. When the order of the edges are defined, the UD-slice edges are defined last, such that this method of encoding is applicable:

```python
class edge_indices(IntEnum):
    UR = 0
    UF = 1
    UL = 2
    UB = 3

    DR = 4
    DF = 5
    DL = 6
    DB = 7

    FR = 8
    FL = 9
    BL = 10
    BR = 11
```

The above describes the following algorithm: 
```python
@property
def POSud_slice_coords(self):
    blank = [False] * 12
    for i, corner in enumerate(self.ep):
        if corner >= 8:
            blank[i] = True

    coord = 0
    count = 3

    for i in range(11, -1, -1):
        if count < 0:
            break

        if blank[i]:
            count -= 1
        else:
            coord += CNK(i, count)

    return coord
```
And the following reverses the above, returning an array for the edge permutation that uses each edge indiscriminatnely, only ensuring that each UD-slice edge is placed correctly such that it can be mapped back to the same index of the co-set:

```python
@POSud_slice_coords.setter
def POSud_slice_coords(self, index):
    count = 3
    self.ep = [False] * 12

    for i in range(11, -1, -1):
        if count < 0:
            break

        v = CNK(i, count)

        if index < v:
            # noinspection PyTypeChecker
            self.ep[i] = 8 + count
            count -= 1
        else:
            index -= v

    others = 0
    for i, edge in enumerate(self.ep):
        if not edge:
            # noinspection PyTypeChecker
            self.ep[i] = others
            others += 1
```

The first phase of the algorithm combines all three of these coordinates, first calculating the coordinates of the cube provided by the user, before searching simultainiously through each one of those co-sets to find a sequence of any moves that take each of the coorindates to (0). 

It is worth noting that the first group's group operations (the moves) are not limited here as they are elsewhere in the algorithm, so for each and every element there are 18 operations that will take you to another element in the group. Whilst searching however, the same move is not allowed to be applied consequentively as this is simply synoymous with another move that is considered a singular move instead of two `self.axis[node_depth - 1] in (axis, axis + 3)`.

# Phase Two
When a sequence of moves has been found that maps the given cube to the identity element of H1, that new cube acts as the new root of the search in phase two. 

Again you attempt to search a subgroup of the Cube group, this time with teh assurance that both the corners and edges are orientated correctly and the UD-slice edges are in their *home-position*. 

Some basic intuitive sees that any single move of the right, front, left or back face will change the orientation of some edges and some corners and shift some of the UD-slice edges out of the UD-slice. It follows therefore that you constrain the search to moves only pertaining to double turns of the front, right, left and back faces such that you maintain the neuatral orientation of the cubes pieces. You can however, still move the up and down faces in single turns as this does not effect any of the aforementioned attributes. 

This again limits the search space as the moves requried to restore a cube from this position is minimal, and the branching factor of the search is significnatly reduced as a result of teh constraints placed on the possible moves. 

You may conclude therefore that the only coordinates that need be mentioned as those that describe the permutation of the pieces on the cube, namely teh corner permutation, the permutation of the UD-slice edges and those edges that do not fall into that group. 

### The edge permutation coordinate

On a cube, there are 12 edges and assume the orientation is constant between them as provided by phase 1, there are `fact 12 - 1 = 479001599` possible permutations for the edges. Even for a modern computer, generating teh tables required to navigate a search space of that size is not a feasable task, therefore the problem is broken down into two sections - the edges of the UD-slice and those contained in the up and down face:

#### The edge8 coordinate

When the edges are defined, a natural order is given to them as shown briefly above. 

Given the nature of a permutation, it follows that you use an ecoding system with a variable base such as the factoradic number system, where each element in a factoradic number is assigned a weight according to `fact weight` and the max size of that digit is `wight - 1`. This is a one to one number sytsem that maps one of `fact 8 - 1 = 40319` permutations to a single coordinate and back again. 

You work from **right to left**, starting from the 8th edge (we ignore those to the right - the UD-slice edges), with a weight of **7 decending**. You look at the edge contained at that position in the permutation `DR` and consider those edges higher in the natural order than it to the left of that edge in the permutation `2`.

You are then able to multiply the weight by the number of edges higher in order than itself, before summing that to the total `7 fact * 2 = 10080` and repeating this process as you work left, ignore the 1st edge in the permutation as that is simply implied by that's left behind.

Like the above encoding methods, the identity element of the group (a solved cube) has the edge permutation coordinate of 0 as all edges are in the defined order, where each edges integer value is higher than that of it's left-adjacent edges.

The following is the algorithm that describes the permutation of the 8 edges in the method described above: 

```python
@property
def P8edge_coords(self):
    coord = 0

    for p in range(7, 0, -1):
        higher = 0
        for edge in self.ep[:p]:
            if edge > self.ep[p]:
                higher += 1

        coord = (coord + higher) * p

    return coord
```

This reverses the above with an intuitive approach:

```python
@P8edge_coords.setter
def P8edge_coords(self, index):
    corners = list(range(8))
    self.ep[:8] = [-1] * 8
    coeffs = [0] * 7
    for i in range(2, 9):
        coeffs[i - 2] = index % i
        index //= i

    for i in range(7, 0, -1):
        self.ep[i] = corners.pop(i - coeffs[i - 1])

    self.ep[0] = corners[0]
```

#### The edge4 permutation coordinate

The edge4 permutation coordintae simply describes the permutation of the edges contained within the UD-slice in an analogous manner to that of the edge8's encoding algorithm where the identity cube has teh corner permutation coordinate of 0, only this time describing the last 4 edges in an array of edges:

```python
@property
def P4edge_coords(self):
    cord = 0
    ep = self.ep[8:]
    for p in range(3, 0, -1):
        higher = 0
        for edge in ep[:p]:
            if edge > ep[p]:
                higher += 1

        cord = (cord + higher) * p

    return cord
```
The reverse:
```python
@P4edge_coords.setter
def P4edge_coords(self, index):
    self.ep[8:] = [-1] * 4

    corners = list(range(8, 12))
    coeffs = [0] * 3
    for i in range(2, 5):
        coeffs[i - 2] = index % i
        index //= i

    for i in range(3, 0, -1):
        self.ep[8 + i] = corners.pop(i - coeffs[i - 1])

    self.ep[8] = corners[0]
```

### The corner permutation coordinate

Again, the permutation of the corners can be described by a coordinate using the factoradic number system: 

```python
@property
def Pcorner_coords(self):
    index = 0
    for p in range(7, 0, -1):
        higher = 0
        for corner in self.cp[:p]:
            if corner > self.cp[p]:
                higher += 1

        index = (index + higher) * p

    return index
```
The contrary:
```python
@Pcorner_coords.setter
def Pcorner_coords(self, index):
    corners = list(range(8))
    self.cp = [-1] * 8
    coeffs = [0] * 7
    for i in range(2, 9):
        coeffs[i - 2] = index % i
        index //= i

    for i in range(7, 0, -1):
        self.cp[i] = corners.pop(i - coeffs[i - 1])

    self.cp[0] = corners[0]
```

Phase two of the solver uses those 3 coordinates to find a sequence of moves that map the identity cube of H1 where the pieces are orientated correctly and the UD-slice edges are in the correct slice, to a solved cube where the permutations of the cubes pieces are corrected.


# Data structures
 

## Facelet level
The cube must first be defined by a 1d string of characters that represent the colours of each of the 54 facelets present on the cube.

They are numbered from **top-down from left to right**, in the order of *axis* as defined here:

```python
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
This is the *identity* definition
