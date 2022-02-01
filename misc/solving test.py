from definitions.cubie_cube import cubiecube
from definitions.facelet_cube import facelet_cube
from initialising.solve import Phase2, Phase1

defs = {"solved": "UUU UUU UUU RRR RRR RRR LLL LLL LLL FFF FFF FFF BBB BBB BBB DDD DDD DDD",
        "random": "BLU RUL LUF LFB DRD FUF RFB BLR BUR DLU BFF DDR LBU RBD DBR FLU RDF DUL"}

c = facelet_cube(defs["random"].replace(" ", ""))
c = c.to_cubeie_cube(cubiecube())
c.shuffle()

print(c.Ocorner_coords, c.Pcorner_coords, c.Oedge_coords, c.Pedge_coords, c.P4edge_coords)

p1 = Phase1(c)
p1.start_search(single=True)
c.MOVE_arr(*p1.q.get())

print(c.Ocorner_coords, c.Pcorner_coords, c.Oedge_coords, c.Pedge_coords, c.POSud_slice_coords)

p2 = Phase2(c)
p2.start_search(single=True)
c.MOVE_arr(*p2.q.get())

print(c.Ocorner_coords, c.Pcorner_coords, c.Oedge_coords, c.Pedge_coords, c.POSud_slice_coords)
