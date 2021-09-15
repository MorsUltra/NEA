# Rubiks cube solver 

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