import queue
import threading

from definitions.cubie_cube import cubiecube
from initialising.table_init import tables


class solver:

    def __init__(self, cube, multithreading=False, workers=5):
        self._running = True
        self.multithreading = multithreading
        self.phase1_searcher = Phase1(cube)
        self.phase2_searcher = Phase2
        self.phase2_searchers = []

        self.cc_data = cube.to_data_arr()

        self.final_solutions = [] if multithreading else None

        self.phase1_thread = threading.Thread(target=self.phase1_searcher.start_search)
        self.phase2_worker_threads = [threading.Thread(target=self.phase2_worker) for _ in range(workers)]

    def find_solutions(self):
        if self.cc_data == ([0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
            return None
        if self.multithreading:
            self.multi_thread_search()

        else:
            self.phase1_searcher.start_search(single=True)
            phase1_solution = self.phase1_searcher.q.get()

            cc = cubiecube(cp=self.cc_data[0], co=self.cc_data[1], ep=self.cc_data[2], eo=self.cc_data[3],
                           moves=phase1_solution)

            phase2_solver = self.phase2_searcher(cc)

            phase2_solver.start_search(single=True)

            phase2_solution = phase2_solver.q.get()

            moves = phase1_solution[0] + phase2_solution[0]
            powers = phase1_solution[1] + phase2_solution[1]

            return [moves, powers]

    def multi_thread_search(self):
        self.phase1_thread.start()

        for worker in self.phase2_worker_threads:
            worker.start()

        checker = threading.Thread(target=self.checker)
        checker.start()

    def phase2_worker(self):
        while self._running:
            if not self.phase1_searcher.q.empty():
                phase1_solution = self.phase1_searcher.q.get()

                cc = cubiecube(cp=self.cc_data[0], co=self.cc_data[1], ep=self.cc_data[2], eo=self.cc_data[3],
                               moves=phase1_solution)

                phase2_searcher = self.phase2_searcher(cc)
                self.phase2_searchers.append(phase2_searcher)

                phase2_searcher.start_search(single=True)

                # When terminated during search won't produce solution so will hang at this .get() if not compensated for
                if not phase2_searcher.q.empty():
                    phase2_solution = phase2_searcher.q.get()

                    moves = phase1_solution[0] + phase2_solution[0]
                    powers = phase1_solution[1] + phase2_solution[1]

                    self.final_solutions.append([moves, powers])

                self.phase1_searcher.q.task_done()

    def checker(self):
        while self._running:
            if not self.phase1_thread.is_alive() and not self.phase1_searcher.q.unfinished_tasks:
                self.terminate()

    def terminate(self):
        self._running = False

        self.phase1_searcher.terminate()

        for searcher in self.phase2_searchers:
            searcher.terminate()


class PhaseN:
    t = tables()

    def __init__(self, cube, length=30):
        self.cube = cube

        self.max = length
        self.moves = [-1] * length
        self.powers = [-1] * length
        self.h_costs = [-1] * length

        self.coordinate1 = [0] * length
        self.coordinate2 = [0] * length
        self.coordinate3 = [0] * length

        self._running = True
        self.q = queue.Queue()

    def terminate(self):
        self._running = False

    @property
    def stats(self):
        axis = [i for i in self.moves if i != -1]
        moves_power = [i for i in self.powers if i != -1]

        return axis, moves_power

    def start_search(self, single=False):
        for lower_bound in range(self.max):
            n = self.ida(0, lower_bound)
            if n > 0:  # do some testing here with solved cubes returning solved at start
                self.q.put(self.stats)
                if single:
                    break
                else:
                    continue

    def h(self, node_depth):
        pass

    def ida(self, node_depth, q):
        pass


class Phase1(PhaseN):

    def __init__(self, cube, length=30):
        super().__init__(cube, length=length)

        self.coordinate1[0] = self.cube.Ocorner_coords
        self.coordinate2[0] = self.cube.Oedge_coords
        self.coordinate3[0] = self.cube.POSud_slice_coords
        self.h_costs[0] = self.h(0)

    def h(self, node_depth):
        return max(
            self.t.UDslice_Oedge_pruning_table[self.coordinate3[node_depth]][self.coordinate2[node_depth]],
            self.t.UDslice_Ocorner_pruning_table[self.coordinate3[node_depth]][self.coordinate1[node_depth]]
        )

    def ida(self, node_depth, q):
        if not self._running:
            return -2

        if self.h(node_depth) == 0:
            return node_depth

        elif self.h_costs[node_depth] <= q:  # If within upper bounds
            for move in range(6):
                # TODO can optimise that 0 designed to fix errors from starting and referencing previous nodes and depths
                if node_depth > 0 and self.moves[node_depth - 1] in (move, move + 3):
                    # if the node is not at the start and
                    continue
                else:
                    for power in range(3):
                        self.moves[node_depth] = move
                        self.powers[node_depth] = power + 1
                        table_index = (move * 3) + power

                        # get the new coords for the connecting node achieved by doing that move with that power
                        self.coordinate1[node_depth + 1] = self.t.Ocorner_table[self.coordinate1[node_depth]][
                            table_index]  # 1: Ocorner
                        self.coordinate2[node_depth + 1] = self.t.Oedge_table[self.coordinate2[node_depth]][
                            table_index]  # 1: Oedge
                        self.coordinate3[node_depth + 1] = \
                            self.t.POSud_slice_table[self.coordinate3[node_depth]][table_index]  # 1: POSudslice

                        # get the cost of the next node
                        self.h_costs[node_depth + 1] = self.h(node_depth + 1)

                        # search the next node defined above with the assumption that you can get closer to the target subgroup
                        continue_search = self.ida(node_depth + 1, q - 1)

                        if continue_search >= 0:
                            return continue_search

        # no more nodes here that get you closer to the target state
        return -1


class Phase2(PhaseN):

    def __init__(self, cube, length=30):
        super().__init__(cube, length=length)

        self.coordinate1[0] = self.cube.P4edge_coords
        self.coordinate2[0] = self.cube.Pcorner_coords
        self.coordinate3[0] = self.cube.P8edge_coords
        self.h_costs[0] = self.h(0)

    def h(self, node_depth):
        return max(
            self.t.P4edge_P8edge_Ptable[self.coordinate1[node_depth]][self.coordinate3[node_depth]],
            self.t.P4edge_Pcorner_Ptable[self.coordinate1[node_depth]][self.coordinate2[node_depth]]
        )

    def ida(self, node_depth, q):
        if not self._running:
            return -2

        if self.h(node_depth) == 0:
            return node_depth

        elif self.h_costs[node_depth] <= q:
            for move in range(6):
                if node_depth > 0 and self.moves[node_depth - 1] in (move, move + 3):
                    continue
                else:
                    for move_power in range(3):
                        if move_power != 1 and move % 5 != 0:
                            continue

                        self.moves[node_depth] = move
                        self.powers[node_depth] = move_power + 1
                        table_index = (move * 3) + move_power

                        self.coordinate1[node_depth + 1] = self.t.P4edge_table[self.coordinate1[node_depth]][
                            table_index]
                        self.coordinate2[node_depth + 1] = self.t.Pcorner_table[self.coordinate2[node_depth]][
                            table_index]
                        self.coordinate3[node_depth + 1] = self.t.P8edge_table[self.coordinate3[node_depth]][
                            table_index]

                        self.h_costs[node_depth + 1] = self.h(node_depth + 1)

                        continue_search = self.ida(node_depth + 1, q - 1)

                        if continue_search >= 0:
                            return continue_search

        return -1
