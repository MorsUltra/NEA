from cubes import facelet_cube
from GUI.pygame_draw_cube import draw
from definitions.moves import *
from definitions.moves import *
from timeit import default_timer as timer
import numpy as np
from time import sleep


class solve():

    moves = [Umove,
             Rmove,
             Lmove,
             Dmove,
             Fmove,
             Bmove]

    def __init__(self, max=30, string=""):
        from table_init import tables
        self.t = tables()
        fc = facelet_cube(string)
        self.cc = fc.to_cubeie_cube()

        self.max = max

        self.axis = [-1] * max
        self.moves_power = [-1] * max

        self.Ocorner_coords = [0] * max
        self.Oedge_coords = [0] * max
        self.POSud_slice_coords = [0] * max

        self.h1_costs = [0] * max

        self.Ocorner_coords[0] = self.cc.Ocorner_coords
        self.Oedge_coords[0] = self.cc.Oedge_coords
        self.POSud_slice_coords[0] = self.cc.POSud_slice_coords

        self.h1_costs[0] = self.h1(0)
        h1 = self.run1()
        print(self.h1_costs)
        print(self.axis)
        print(self.moves_power)
        self.phase2_init(h1)
        h2 = self.run2()
        print(self.h2_costs)
        print(self.axis2)
        print(self.moves_power2)


    def run1(self):
        count = 0
        for lower_bound in range(self.max):

            print("LOWER BOUND-------------------------: {}".format(lower_bound))
            n = self.phase_1(0, lower_bound)
            if n > 0:
                count += 1
                if count == 1:
                    print(n)
                    break

        return n

    def run2(self):
        for lower_bound in range(self.remaining_moves):
            print("LOWER BOUND-------------------------: {}".format(lower_bound))
            n = self.phase_2(0, lower_bound)
            if n > 0:
                print(n)
                break

    def phase_1(self, node_depth, q):
        if self.h1(node_depth) == 0:  # if a cube has been found in H0
            return node_depth
        elif self.h1_costs[node_depth] <= q:  # if within lower bounds
            for axis in range(6):
                # can optimise that 0 designed to fix errors from starting and referencing previous nodes and depths
                if node_depth > 0 and self.axis[node_depth - 1] in (axis, axis + 3):
                    # if the node is not at the start and
                    continue
                else:
                    for move_power in range(3):
                        self.axis[node_depth] = axis
                        self.moves_power[node_depth] = move_power + 1
                        table_index = axis * 3 + move_power

                        # get the new coords for the conneting node achieved by doing that move with that power
                        self.Ocorner_coords[node_depth + 1] = self.t.Ocorner_table[self.Ocorner_coords[node_depth]][table_index]
                        self.Oedge_coords[node_depth + 1] = self.t.Oedge_table[self.Oedge_coords[node_depth]][table_index]
                        self.POSud_slice_coords[node_depth + 1] = self.t.POSud_slice_table[self.POSud_slice_coords[node_depth]][table_index]

                        # get the cost of the next node
                        self.h1_costs[node_depth + 1] = self.h1(node_depth + 1)

                        # search the next node defined above with the assumption that you can get closer to the target subgroup
                        continue_search = self.phase_1(node_depth + 1, q - 1)

                        if continue_search >= 0:
                            return continue_search

        # no more nodes here that get you closer to the target state
        return -1

    def phase2_init(self, n):
        #set new cube from start position
        cc = self.cc
        for i, move in enumerate(self.axis):
            if move == -1:
                continue
            for power in range(self.moves_power[i]):
                cc.MOVE(self.moves[move])

        self.remaining_moves = self.max-n

        self.axis2 = [-1] * self.remaining_moves
        self.moves_power2 = [-1] * self.remaining_moves

        self.Pedge4_coords = [0] * self.remaining_moves
        self.Pcorner_coords = [0] * self.remaining_moves
        self.Pedge8_coords = [0] * self.remaining_moves

        self.h2_costs = [0] * self.remaining_moves

        self.Pedge4_coords[0] = cc.P4edge_coords
        self.Pcorner_coords[0] = cc.Pcorner_coords
        self.Pedge8_coords[0] = cc.P8edge_coords

        self.h2_costs[0] = self.h2(0)

    def phase_2(self, node_depth, q):
        if self.h2(node_depth) == 0:  # if a cube has been found in solved state
            return node_depth
        elif self.h2_costs[node_depth] <= q:  # if within lower bounds
            for axis in range(6):
                # can optimise that 0 designed to fix errors from starting and referencing previous nodes and depths
                if node_depth > 0 and self.axis[node_depth - 1] in (axis, axis + 3):
                    # if the node is not at the start and
                    continue
                else:
                    for move_power in range(3):
                        if move_power != 1 and axis % 3 != 0:
                            continue
                        self.axis2[node_depth] = axis
                        self.moves_power2[node_depth] = move_power + 1
                        table_index = axis * 3 + move_power

                        # get the new coords for the conneting node achieved by doing that move with that power
                        self.Pedge4_coords[node_depth + 1] = self.t.P4edge_table[self.Pedge4_coords[node_depth]][table_index]
                        self.Pcorner_coords[node_depth + 1] = self.t.Pcorner_table[self.Pcorner_coords[node_depth]][table_index]
                        self.Pedge8_coords[node_depth + 1] = self.t.P8edge_table[self.Pedge8_coords[node_depth]][table_index]

                        # get the cost of the next node
                        self.h2_costs[node_depth + 1] = self.h2(node_depth + 1)

                        # search the next node defined above with the assumption that you can get closer to the target subgroup
                        continue_search = self.phase_2(node_depth + 1, q - 1)

                        if continue_search >= 0:
                            return continue_search

        # no more nodes here that get you closer to the target state
        return -1

    def h1(self, node_depth):
        return max(
            self.t.UDslice_Oedge_pruning_table[self.POSud_slice_coords[node_depth]][self.Oedge_coords[node_depth]],
            self.t.UDslice_Ocorner_pruning_table[self.POSud_slice_coords[node_depth]][self.Ocorner_coords[node_depth]]
        )

    def h2(self, node_depth):
        return max(
            self.t.P4edge_P8edge_Ptable[self.Pedge4_coords[node_depth]][self.Pedge8_coords[node_depth]],
            self.t.P4edge_Pcorner_Ptable[self.Pedge4_coords[node_depth]][self.Pcorner_coords[node_depth]]
        )

string_def = "LUF FUF FLF UUU DRL RRD BDL ULL DRB DDR BFB RUF LBU FBR RRL ULD FDD BBB"
string_def = "UUU UUU UUU BLF RRR RRR LRL LLL LLL FFR FFF FFF RBB BBB BBB DDD DDD DDD"
string_def = string_def.replace(" ", "")

solve(string=string_def)
