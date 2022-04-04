import queue

from definitions.cubie_cube import CubieCube
from initialising.table_init import Tables


class Solver:
    def __init__(self, cube):
        self.cc = cube

        self.phase1_searcher = Phase1
        self.phase2_searcher = Phase2

        self.cc_data = cube.to_data_arrary()

        self.final_solutions = []

        self._running = True

    def find_solutions(self):
        if self.cc.is_solved():
            return None

        else:
            phase1 = self.phase1_searcher(self.cc)
            phase1.start_search()
            phase1_solution = phase1.q.get()

            cc = CubieCube(data=self.cc_data,
                           moves=phase1_solution)

            phase2 = self.phase2_searcher(cc)
            phase2.start_search()
            phase2_solution = phase2.q.get()

            moves = phase1_solution[0] + phase2_solution[0]
            powers = phase1_solution[1] + phase2_solution[1]

            return [moves, powers]


class PhaseN:
    """
    This is an abstract class for the phases. Both Phase 1 and Phase 2 follow a similar process, however there
    are nuances between the two in some methods that much be overridden.
    """

    # Load/generate the move and pruning tables required to perform the search and use the heuristic
    t = Tables()

    # def __init__(self, cube: CubieCube, length: int = 30):
    def __init__(self, cube: CubieCube, length: int = 30):
        """
        Constructs empty lists and attributes required for the search.

        :param cube: CubieCube object that is the root of the search for this phase.
        :param length: integer that serves as the maximum length of the search.
        """

        self.cube: CubieCube = cube

        self.max_depth: int = length

        # Create empty lists to hold the "history" of the search.
        self.moves: list[int] = [-1] * length  # The history of the side that's being turned.
        self.powers: list[int] = [-1] * length  # The history of the number of the times as side is being turned.
        self.h_costs: list[int] = [-1] * length  # The history of the costs for each step.

        self.coordinate1: list[int] = [0] * length  # The history of the first coordinate associated with Phase N
        self.coordinate2: list[int] = [0] * length  # The history of the second coordinate associated with Phase N
        self.coordinate3: list[int] = [0] * length  # The history of the third coordinate associated with Phase N

        # Create the list to hold solutions when found (compatible with multithreading implementations.
        self.q = queue.Queue()

    @property
    def stats(self):
        """
        Function is used to get the actions - moves and their powers - associated with the search.

        :return: Stats associated with the search - what moves have been performed with what power.
        """

        moves = [i for i in self.moves if i != -1]
        powers = [i for i in self.powers if i != -1]

        if not moves and not powers:  # If search has not been executed.
            return None
        else:
            return moves, powers

    def start_search(self):
        """
        Method to perform the search of Phase N. Handles iterating upper bound on depth of search.

        :return: None
        """

        for lower_bound in range(self.max_depth):
            n = self.ida(0, lower_bound)
            if n > 0:  # If the search has found a solution.
                self.q.put(self.stats)  # Place solution in the queue.
                return

    def h(self, node_depth: int) -> int:
        """
        Abstract function for heuristic used in Phase N search to provide a lower bound on the number of moves
        required to solve a position.

        :param node_depth: node depth used to look up current position of cube and relevant coordinates.
        :return: Lower bound on number of moves required to solve position at node_depth.
        """

        ...

    def ida(self, node_depth: int, q: int) -> int:
        """
        Abstract function for iterative depth search to find solutions for Phase N.

        :param node_depth:
        :param q:
        :return: -1 if no solution found at current position; n > 0 if solution found.
        """

        ...


class Phase1(PhaseN):
    """
    Subclass for managing the search of the first phase of the Two-Phase Algorithm.
    """

    def __init__(self, *args, **kwargs):
        """
        Sets root of search with Phase 1 coordinates in preparation for search and retrieves initial cost.
        """

        super().__init__(*args, **kwargs)

        # Initialising the first coordinates and costs using phase 1 coordinates.
        self.coordinate1[0] = self.cube.Ocorner_coords
        self.coordinate2[0] = self.cube.Oedge_coords
        self.coordinate3[0] = self.cube.POSud_slice_coords

        self.h_costs[0] = self.h(0)  # Get cost of starting position

    def h(self, node_depth: int) -> int:
        """
        Function to provide a lower bound on the number of moves
        required to solve a position in Phase 1.

        :param node_depth: node depth used to look up current position of cube and relevant coordinates.
        :return: Lower bound on number of moves required to solve position at node_depth.
        """

        return max(
            self.t.UDslice_Oedge_pruning_table[self.coordinate3[node_depth]][self.coordinate2[node_depth]],
            self.t.UDslice_Ocorner_pruning_table[self.coordinate3[node_depth]][self.coordinate1[node_depth]]
        )

    def ida(self, node_depth: int, q: int) -> int:
        """
        Function for performing search to find solutions for Phase N.

        :param node_depth:
        :param q:
        :return: -1 if no solution found at current position; n > 0 if solution found.
        """

        # Check if the position has reached the subgroup H1.
        if self.h(node_depth) == 0:  #
            # Backtrack and end search.
            return node_depth

        # If, assuming a perfect solution equal to the lower-bounded cost of this position, this path will exceed the
        # upper bound on depth. Else, prune branch of search.
        elif self.h_costs[node_depth] <= q:
            # Perform the moves on each of the faces <U, L, R, F, B, D>.
            for move in range(6):
                # TODO can optimise that 0 designed to fix errors from starting and referencing previous nodes and depths
                # If this is not the first move and if this move is not synonymous with the last move performed.
                if node_depth > 0 and self.moves[node_depth - 1] in (move, move + 3):
                    continue
                # If move is not a repeat
                else:
                    # Perform each move 3 times to cover a single turn, a double turn,
                    # and an inverse turn (3 single turns).
                    for power in range(3):

                        # Record the move and power performed
                        self.moves[node_depth] = move
                        self.powers[node_depth] = power + 1

                        # Calculate the position in the move tabel this move and power corresponds to.
                        table_index = (move * 3) + power

                        # Look up the coordinates of the cube state after the move is performed and update lists.
                        self.coordinate1[node_depth + 1] = self.t.Ocorner_table[self.coordinate1[node_depth]][
                            table_index]
                        self.coordinate2[node_depth + 1] = self.t.Oedge_table[self.coordinate2[node_depth]][table_index]
                        self.coordinate3[node_depth + 1] = self.t.POSud_slice_table[self.coordinate3[node_depth]][
                            table_index]

                        # Update cost given new position
                        self.h_costs[node_depth + 1] = self.h(node_depth + 1)

                        # Continue to next node.
                        continue_search = self.ida(node_depth + 1, q - 1)

                        # If successive searches yielded a solution.
                        if continue_search >= 0:
                            # Backtrack
                            return continue_search

        # If node exceeds depth of iterative depth.
        return -1


class Phase2(PhaseN):
    """
    Subclass for managing the search of the first phase of the Two-Phase Algorithm.
    """

    def __init__(self, *args, **kwargs):
        """
        Sets root of search with Phase 2 coordinates in preparation for search and retrieves initial cost.
        """
        super().__init__(*args, **kwargs)

        # Initialising the first coordinates and costs using phase 1 coordinates.
        self.coordinate1[0] = self.cube.P4edge_coords
        self.coordinate2[0] = self.cube.Pcorner_coords
        self.coordinate3[0] = self.cube.P8edge_coords

        self.h_costs[0] = self.h(0)  # Get cost of starting position

    def h(self, node_depth: int) -> int:
        """
        Function to provide a lower bound on the number of moves
        required to solve a position in Phase 1.

        :param node_depth: node depth used to look up current position of cube and relevant coordinates.
        :return: Lower bound on number of moves required to solve position at node_depth.
        """

        return max(
            self.t.P4edge_P8edge_Ptable[self.coordinate1[node_depth]][self.coordinate3[node_depth]],
            self.t.P4edge_Pcorner_Ptable[self.coordinate1[node_depth]][self.coordinate2[node_depth]]
        )

    def ida(self, node_depth: int, q: int) -> int:
        """
        Function for performing search to find solutions for Phase N.

        :param node_depth:
        :param q:
        :return: -1 if no solution found at current position; n > 0 if solution found.
        """

        # Check if the position is solved.
        if self.h(node_depth) == 0:
            # Backtrack and end search.
            return node_depth

        # If, assuming a perfect solution equal to the lower-bounded cost of this position, this path will exceed the
        # upper bound on depth. Else, prune branch of search.
        elif self.h_costs[node_depth] <= q:
            # Perform the moves on each of the faces <U, L, R, F, B, D>.
            for move in range(6):
                # If this is not the first move and if this move is not synonymous with the last move performed.
                if node_depth > 0 and self.moves[node_depth - 1] in (move, move + 3):
                    continue
                # If move is not a repeat
                else:
                    # Perform each move 3 times to cover a single turn, a double turn,
                    # and an inverse turn (3 single turns).
                    for move_power in range(3):
                        # If move is not a double and not performed on the <U, D> faces.
                        if move_power != 1 and move % 5 != 0:
                            continue

                        # If the move will maintain the position being in the subgroup H1.
                        # Record the move and power performed
                        self.moves[node_depth] = move
                        self.powers[node_depth] = move_power + 1

                        # Calculate the position in the move tabel this move and power corresponds to.
                        table_index = (move * 3) + move_power

                        # Look up the coordinates of the cube state after the move is performed and update lists.
                        self.coordinate1[node_depth + 1] = self.t.P4edge_table[self.coordinate1[node_depth]][
                            table_index]
                        self.coordinate2[node_depth + 1] = self.t.Pcorner_table[self.coordinate2[node_depth]][
                            table_index]
                        self.coordinate3[node_depth + 1] = self.t.P8edge_table[self.coordinate3[node_depth]][
                            table_index]

                        # Update cost given new position
                        self.h_costs[node_depth + 1] = self.h(node_depth + 1)

                        # Continue to next node.
                        continue_search = self.ida(node_depth + 1, q - 1)

                        # If successive searches yielded a solution.
                        if continue_search >= 0:
                            # Backtrack
                            return continue_search

        # If node exceeds depth of iterative depth.
        return -1
