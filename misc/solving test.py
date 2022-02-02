from definitions.cubie_cube import CubieCube
from definitions.facelet_cube import facelet_cube
from initialising.solve import Phase2, Phase1, Solver

defs = {"solved": "UUU UUU UUU RRR RRR RRR LLL LLL LLL FFF FFF FFF BBB BBB BBB DDD DDD DDD",
        "random": "BLU RUL LUF LFB DRD FUF RFB BLR BUR DLU BFF DDR LBU RBD DBR FLU RDF DUL"}

c = facelet_cube(defs["random"].replace(" ", ""))
c = c.to_cubeie_cube(CubieCube())
c.shuffle()

print(c.Ocorner_coords, c.Pcorner_coords, c.Oedge_coords, c.Pedge_coords, c.P4edge_coords)

s = Solver(c)
solution = s.find_solutions()

c.MOVE_arr(*solution)

print(c.Ocorner_coords, c.Pcorner_coords, c.Oedge_coords, c.Pedge_coords, c.P4edge_coords)
