from initialising.cubes import cubiecube, facelet_cube
from definitions.moves import *
from GUI.pygame_draw_cube import draw

string_def = "UUU UUU UUU BLF RRR RRR LRL LLL LLL FFR FFF FFF RBB BBB BBB DDD DDD DDD".replace(" ", "")
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

move(cc, [0, 4, 0, 4, 3, 1, 5, 0, 5, 3, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [1, 2, 3, 2, 1, 2, 2, 1, 2, 3, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1])

draw(cc.to_facelet_cube())
