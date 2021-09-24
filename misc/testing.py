from initialising.cubes import cubiecube, facelet_cube
from definitions.moves import *
from GUI.pygame_draw_cube import draw

string_def = "UBFFUFBBDRURRRLRFLFDUFLDDRDRUBBFDBBFULLDBRBUFLRDUDLLLU".replace(" ", "")
fc = facelet_cube(string_def)
cc = fc.to_cubeie_cube()
moves = [Umove,
         Rmove,
         Lmove,
         Dmove,
         Fmove,
         Bmove]

def move(cc, axis, moves_power):
    for i, move in enumerate(axis):
        if move == -1:
            continue
        for power in range(moves_power[i]):
            cc.MOVE(moves[move])

print(cc.Oedge_coords, cc.Ocorner_coords, cc.POSud_slice_coords)
move(cc,[2, 4, 5, 3, 2, 5, 1, 4, 5, 1], [3, 3, 2, 3, 1, 1, 3, 1, 2, 1])
print(cc.Oedge_coords, cc.Ocorner_coords, cc.POSud_slice_coords)
move(cc,[4, 3, 4, 0, 2, 3, 2, 0, 1, 5, 3, 5, 0], [2, 1, 2, 2, 2, 1, 2, 3, 2, 2, 1, 2, 1])
print(cc.Oedge_coords, cc.Ocorner_coords, cc.POSud_slice_coords)
draw(cc.to_facelet_cube())
