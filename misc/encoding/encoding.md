# Encoding
Encoding can be used to define the state of any cube. **_Index numbers_** can be used to describe the state of various attributes of the cube. 

In this case, we used **_index numbers_** to describe the permutation and orientation of both the corners and the edges. 

###There are 12 **edges**: 
- Each edge has an orientation `o`, `o ∈ {0, 1}`
  - Edge is not flipped where `o = 0`
  - The orientation of each edge is binary, therefore the binary number system is used to encoding the orientation of all the edges.
    - There are `2^11 - 1 -> 2047` variations.  
    - For example, `1084 -> 10000111100(1)` where the `(1)` is appended to the end as the last edge is dictated by the other 11. The sum of all orientations must be even; one edge cannot be uniquely flipped. By appending the final bit to the end of the orientation when converting between the two, index numbers can only describe valid edge orientations, and exclude those that would not be solvable using traditional means.
- Due to nature of permutations, the factorial number system is used to encode each permutation of the edges, but is reversed in each case.
  - The edges have an inherent hierarchy as described in `permutation_encoding.py`.
    - The factoradic number assigned to each permutation is a function of how many preceding edges are higher in this hierarchy.
      - The highest value possible at `ith` place from the right is therefore `8-i`, as there are 8 edges, one of which is not described in the factoradic number and instead encoded through exhaustion. The highest index number is `479001599 -> 1234567891011!` in factoradic form.

###There are 8 **corners**:
- The orientation and permutation of the corners is encoded in an analogous manner.
  - Instead of the binary number system however, the ternary number system is used to encode the orientation of the corners, where each corner has an orientation `o`, `o ∈ {0, 1, 2}}`.
    - There are 3^7 - 1 -> 2186 variations, where the final bit of the 8-bit number is appended such that `sum(bits) % 3 = 0`.
- Factoradic numbers are also used to encode the corners, where there are `8! - 1 -> 40319` variations and a natural order exists such that corners can be described by how many corners left of them are higher in said hierarchy.
