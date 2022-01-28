from initialising.solve import solver
from definitions.cubie_cube import cubiecube
c = cubiecube()
c.shuffle()
s = solver(c)
solutions = s.find_solutions()

print(c.Ocorner_coords, c.Pcorner_coords, c.Oedge_coords, c.Pedge_coords, c.P4edge_coords)
c.MOVE_arr(*solutions)
print(c.Ocorner_coords, c.Pcorner_coords, c.Oedge_coords, c.Pedge_coords, c.POSud_slice_coords)
# TODO huge fucking bug here no idea what's going on, something in phase two is going wrong.
