from definitions.cubie_cube import *
from definitions.facelet_cube import facelet_cube

# [1869,    1653,   1653,   1627,   1627,   1147,   391,    400,    426,    412
# [1524,    1908,   1906,   1907,   823,    273,    145,    137,    0,      0,
# [366,     368,    413,    413,    406,    418,    415,    409,    96,     91


defs = {"solved": "UUU UUU UUU RRR RRR RRR LLL LLL LLL FFF FFF FFF BBB BBB BBB DDD DDD DDD",
        "random": "BLU RUL LUF LFB DRD FUF RFB BLR BUR DLU BFF DDR LBU RBD DBR FLU RDF DUL"}

c = facelet_cube(defs["random"].replace(" ", ""))
c = c.to_cubeie_cube(CubieCube())

# up back down right back up front down front right


# for move, power in moves:
#     for x in range(power):
#         c.MOVE(MOVES[move])
#     print(c.Ocorner_coords, c.Oedge_coords, c.POSud_slice_coords)

moves = zip([0, 4, 5, 1, 4, 0, 3, 5, 3, 2],
            [2, 2, 2, 3, 3, 1, 3, 3, 3, 1])
MOVES = [Umove, Rmove, Lmove, Fmove, Bmove, Dmove]
c = facelet_cube(defs["random"].replace(" ", ""))
c = c.to_cubeie_cube(CubieCube())

from initialising.solve import Solver
s = Solver(c)
s.find_solutions()
