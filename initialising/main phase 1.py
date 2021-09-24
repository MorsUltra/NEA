# from GUI.pygame_draw_cube import draw
from definitions.moves import *
from definitions.facelet_cube import facelet_cube
from definitions.cubie_cube import cubiecube
from table_init import tables
from pprint import pprint
import time
import queue
import threading


class solver():

    def __init__(self, cube, multithreading=False):
        self._running = True
        self.phase1 = phase1(cube)
        self.phase2 = phase2
        self.cc = cube
        self.final_solutions = [] if multithreading else None
        self.multithreading = multithreading
        self.solution_count = 0

    def solve(self):
        if self.multithreading:
            self.multi()

        else:
            self.phase1.depth_search()

        return None

    def multi(self):
        # start phase 1 which starts appending things to it's queue
        self.phase1_thread = threading.Thread(target=self.phase1.depth_search)
        self.phase1_thread.start()
        # start phase 2 workers which will work through the solutions in phase 1 as they occur
        self.phase2_workers1 = threading.Thread(target=self.phase2_worker, args=(self.cc,))
        # self.phase2_workers2 = threading.Thread(target=self.phase2_worker, args=(self.cc,))
        self.phase2_workers1.start()
        # self.phase2_workers2.start()
        # checker to terminate process if all phase 1 solutions have been found
        #checker = threading.Thread(target=self.checker)

    def phase2_worker(self, cc):
        # phase1.solutions holds current solutions to phase 1
        while self._running:
            phase1 = self.phase1.q.get()  # get solution to phase 1

            cc.MOVE_arr(*phase1)

            print("coords", cc.Ocorner_coords, cc.Oedge_coords) # TODO I think there's a bug with the coordinate tables somewhere? It keeps producing random coordinate pairs that are making no sense


            print("phase 2 searching")
            phase2_solver = self.phase2(cc) # TODO need to clean up how this works with passing solutions between the objects
            phase2_solver.depth_search()

            phase2_solution = phase2_solver.q.get()
            phase2_solver.q.task_done()

            self.final_solutions.append(zip(phase1, phase2_solution))

            self.phase1.q.task_done()
            print("Phase 2 thread completed")

    def checker(self):
        while True:
            if not self.phase1_thread.isAlive() and self.solution_count == len(self.solutions):
                self.terminate()

    def terminate(self):
        self._running = False  # shuts down workers
        self.phase1.terminate()  # stops IDA* search
        #self.phase2.terminate()  # stops IDA* search


class phase_searcher:
    t = tables()

    def __init__(self, cube, length=30):
        self.cube = cube

        self.max = length
        self.axis = [-1] * length
        self.moves_power = [-1] * length
        self.h_costs = [-1] * length

        self.coord1 = [0] * length
        self.coord2 = [0] * length
        self.coord3 = [0] * length

        self._running = True
        self.q = queue.Queue()

    def terminate(self):
        self._running = False

    @property
    def stats(self):
        axis = [i for i in self.axis if i != -1]
        moves_power = [i for i in self.moves_power if i != -1]

        return axis, moves_power

    def depth_search(self):
        for lower_bound in range(self.max):
            #print(f"Lower bound-----------------: {lower_bound}")
            n = self.ida(0, lower_bound)
            if n > 0:
                self.q.put(self.stats)

    def h(self, node_depth):
        pass

    def ida(self, node_depth, q):
        pass


class phase1(phase_searcher):

    def __init__(self, cube, length=30):
        super().__init__(cube, length=length)

        self.coord1[0] = self.cube.Ocorner_coords
        self.coord2[0] = self.cube.Oedge_coords
        self.coord3[0] = self.cube.POSud_slice_coords
        self.h_costs[0] = self.h(0)

    def h(self, node_depth):
        return max(
            self.t.UDslice_Oedge_pruning_table[self.coord3[node_depth]][self.coord2[node_depth]],
            self.t.UDslice_Ocorner_pruning_table[self.coord3[node_depth]][self.coord1[node_depth]]
        )

    def ida(self, node_depth, q):
        if self.h(node_depth) == 0:
            return node_depth

        if not self._running:
            return -2

        elif self.h_costs[node_depth] <= q:  # if within lower bounds
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

                        # get the new coords for the connecting node achieved by doing that move with that power
                        self.coord1[node_depth + 1] = self.t.Ocorner_table[self.coord1[node_depth]][
                            table_index]  # 1: Ocorner
                        self.coord2[node_depth + 1] = self.t.Oedge_table[self.coord2[node_depth]][
                            table_index]  # 1: Oedge
                        self.coord3[node_depth + 1] = \
                            self.t.POSud_slice_table[self.coord3[node_depth]][table_index]  # 1: POSudslice

                        # get the cost of the next node
                        self.h_costs[node_depth + 1] = self.h(node_depth + 1)

                        # search the next node defined above with the assumption that you can get closer to the target subgroup
                        continue_search = self.ida(node_depth + 1, q - 1)

                        if continue_search >= 0:
                            return continue_search

        # no more nodes here that get you closer to the target state
        return -1


class phase2(phase_searcher):

    def __init__(self, cube, length=30):
        super().__init__(cube, length=length)

        self.coord1[0] = self.cube.P4edge_coords
        self.coord2[0] = self.cube.Pcorner_coords
        self.coord3[0] = self.cube.P8edge_coords
        self.h_costs[0] = self.h(0)

    def depth_search(self):
        for lower_bound in range(self.max):
            print(f"Lower bound-----------------: {lower_bound}")
            n = self.ida(0, lower_bound)
            if n > 0:
                self.q.put(self.stats)
                break

    def h(self, node_depth):
        return max(
            self.t.P4edge_P8edge_Ptable[self.coord1[node_depth]][self.coord3[node_depth]],
            self.t.P4edge_Pcorner_Ptable[self.coord1[node_depth]][self.coord2[node_depth]]
        )

    def ida(self, node_depth, q):
        if self.h(node_depth) == 0:
            return node_depth

        if not self._running:
            return -2

        elif self.h_costs[node_depth] <= q:  # if within lower bounds
            for axis in range(6):
                # can optimise that 0 designed to fix errors from starting and referencing previous nodes and depths
                if node_depth > 0 and self.axis[node_depth - 1] in (axis, axis + 3):
                    # if the node is not at the start and
                    continue
                else:
                    for move_power in range(3):
                        if move_power != 1 and axis % 3 != 0:
                            continue

                        self.axis[node_depth] = axis
                        self.moves_power[node_depth] = move_power + 1
                        table_index = axis * 3 + move_power

                        # get the new coords for the conneting node achieved by doing that move with that power
                        self.coord1[node_depth + 1] = self.t.P4edge_table[self.coord1[node_depth]][
                            table_index]  # Pedge4_coords
                        self.coord2[node_depth + 1] = self.t.Pcorner_table[self.coord2[node_depth]][
                            table_index]  # Pcorner_coords
                        self.coord3[node_depth + 1] = self.t.P8edge_table[self.coord3[node_depth]][
                            table_index]  # Pedge8_coords

                        # get the cost of the next node
                        self.h_costs[node_depth + 1] = self.h(node_depth + 1)

                        # search the next node defined above with the assumption that you can get closer to the target subgroup
                        continue_search = self.ida(node_depth + 1, q - 1)

                        if continue_search >= 0:
                            return continue_search

        # no more nodes here that get you closer to the target state
        return -1


defs = {"solved": "UUU UUU UUU RRR RRR RRR LLL LLL LLL FFF FFF FFF BBB BBB BBB DDD DDD DDD",
        "random": "BLU RUL LUF LFB DRD FUF RFB BLR BUR DLU BFF DDR LBU RBD DBR FLU RDF DUL"}

c = facelet_cube(defs["random"].replace(" ", ""))
c = c.to_cubeie_cube(cubiecube())

s = solver(c, multithreading=True)
s.solve()

while True:
    print(s.phase1.q.qsize())

    time.sleep(4)
    print(s.final_solutions)



