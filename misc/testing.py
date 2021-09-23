from initialising.cubes import cubiecube, facelet_cube
from definitions.moves import *
from GUI.pygame_draw_cube import draw

string_def = "LUF FUF FLF UUU DRL RRD BDL ULL DRB DDR BFB RUF LBU FBR RRL ULD FDD BBB".replace(" ", "")
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
move(cc,[4, 0, 2, 4, 3, 1, 4, 2, 1],[3, 2, 2, 3, 1, 3, 1, 1, 1])
print(cc.Oedge_coords, cc.Ocorner_coords, cc.POSud_slice_coords)
draw(cc.to_facelet_cube())
