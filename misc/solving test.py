from definitions.cubie_cube import cubiecube
from definitions.facelet_cube import facelet_cube
from initialising.solve import solver

defs = {"solved": "UUU UUU UUU RRR RRR RRR LLL LLL LLL FFF FFF FFF BBB BBB BBB DDD DDD DDD",
        "random": "BLU RUL LUF LFB DRD FUF RFB BLR BUR DLU BFF DDR LBU RBD DBR FLU RDF DUL"}

c = facelet_cube(defs["random"].replace(" ", ""))
c = c.to_cubeie_cube(cubiecube())
c.shuffle()
s = solver(c)
phase1 = s.find_solutions()

print(c.Ocorner_coords, c.Pcorner_coords, c.Oedge_coords, c.Pedge_coords, c.P4edge_coords)
c.MOVE_arr(*phase1)
print(c.Ocorner_coords, c.Pcorner_coords, c.Oedge_coords, c.Pedge_coords, c.POSud_slice_coords)

from initialising.solve import phase2

p2 = phase2(c)
phase2_solution = p2.find_solutions(single=True)
print(c.Ocorner_coords, c.Pcorner_coords, c.Oedge_coords, c.Pedge_coords, c.P4edge_coords)
c.MOVE_arr(*phase2_solution)
print(c.Ocorner_coords, c.Pcorner_coords, c.Oedge_coords, c.Pedge_coords, c.POSud_slice_coords)
# TODO huge fucking bug here no idea what's going on, something in phase two is going wrong.
