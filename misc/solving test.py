from definitions.cubie_cube import CubieCube
from definitions.facelet_cube import FaceletCube
from initialising.solve import Solver

defs = {"solved": "UUU UUU UUU RRR RRR RRR LLL LLL LLL FFF FFF FFF BBB BBB BBB DDD DDD DDD",
        "random": "BLU RUL LUF LFB DRD FUF RFB BLR BUR DLU BFF DDR LBU RBD DBR FLU RDF DUL"}

c = FaceletCube(defs["random"].replace(" ", ""))
c = c.to_cubeie_cube(CubieCube())
c.shuffle()

print(c.o_corner_coords, c.p_corner_coords, c.o_edge_coords, c.p_edge_coords, c.p_4edge_coords)

s = Solver(c)
solution = s.find_solutions()

c.apply_move_array(*solution)

print(c.o_corner_coords, c.p_corner_coords, c.o_edge_coords, c.p_edge_coords, c.p_4edge_coords)
