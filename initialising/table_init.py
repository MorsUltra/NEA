import os

import numpy as np

from definitions.cubie_cube import CubieCube

CubieCube.create_moves()


class Tables:
    NO_Ocorner_coords = 2187
    NO_Pcorner_coords = 40320

    NO_Oedge_coords = 2048

    NO_POSud_slice_coords = 495

    NO_P4edge_coords = 24
    NO_P8edge_coords = 40320

    moves = CubieCube.MOVES

    save_file_name = r"\Pruning tables.npz"

    def __init__(self, load=True, save=True):
        table_file_path = os.getcwd() + self.save_file_name

        self.Ocorner_table = []
        self.Pcorner_table = []
        self.Oedge_table = []
        self.POSud_slice_table = []
        self.P4edge_table = []
        self.P8edge_table = []

        self.UDslice_Oedge_pruning_table = []
        self.UDslice_Ocorner_pruning_table = []

        self.P4edge_P8edge_Ptable = []
        self.P4edge_Pcorner_Ptable = []

        print(table_file_path)

        if os.path.isfile(table_file_path) and load:
            print("loading lookup tables")

            self.load_file(table_file_path)

        else:
            print("creating lookup tables")

            self.create_tables()

            if save:
                data = [self.Ocorner_table,
                        self.Pcorner_table,
                        self.Oedge_table,
                        self.POSud_slice_table,
                        self.UDslice_Oedge_pruning_table,
                        self.UDslice_Ocorner_pruning_table,

                        self.P4edge_table,
                        self.P8edge_table,
                        self.P4edge_P8edge_Ptable,
                        self.P4edge_Pcorner_Ptable]
                self.save_file(table_file_path, data)

    def create_tables(self):
        self.create_Ocorner_table()
        self.create_Oedge_table()
        self.create_POSud_slice_table()
        self.create_UDslice_Ocorner_Ptable()
        self.create_UDslice_Oedge_Ptable()

        self.create_Pcorner_table()
        self.create_P8edge_table()
        self.create_P4edge_table()
        self.create_P4edge_P8edge_Ptable()
        self.create_P4edge_Pcorner_Ptable()

    @staticmethod
    def save_file(path, data):
        np.savez(path, *data)

    def load_file(self, filename):
        x = np.load(filename)
        # noinspection PyUnresolvedReferences
        names = sorted(x.files)

        self.Ocorner_table = x[names[0]].tolist()
        self.Pcorner_table = x[names[1]].tolist()
        self.Oedge_table = x[names[2]].tolist()
        self.POSud_slice_table = x[names[3]].tolist()
        self.UDslice_Oedge_pruning_table = x[names[4]].tolist()
        self.UDslice_Ocorner_pruning_table = x[names[5]].tolist()

        self.P4edge_table = x[names[6]].tolist()
        self.P8edge_table = x[names[7]].tolist()
        self.P4edge_P8edge_Ptable = x[names[8]].tolist()
        self.P4edge_Pcorner_Ptable = x[names[9]].tolist()

    # Phase 1 moves tables
    def create_Ocorner_table(self):
        """
        Method to create the move table for corner orientation.
        """

        # Create blank cube to use for move table creation.
        cc = CubieCube()

        # Create a blank template - 1 coordinate of the 2187 corner orientation permutations can be mapped to 18
        # other corner orientation coordinates.
        template = [[-1] * 18 for _ in range(self.NO_Ocorner_coords)]

        # For every one of the 2187 corner orientation permutations.
        for coord in range(self.NO_Ocorner_coords):
            # For every one of the 6 possible moves.
            for i, move in enumerate(self.moves):
                # Set the cube to that permutation.
                cc.o_corner_coords = coord
                # For every power of each move.
                for power in range(3):
                    # Apply the move, concerning only the orientation of the corners and ignore the permutation to
                    # save time.
                    cc.corner_orientation_move(move)
                    # Record which corner orientation coordinates the permutation is mapped to by the move. Abstract
                    # out every other piece of data.
                    template[coord][(3 * i) + power] = cc.o_corner_coords

        # Load the table into memory.
        self.Ocorner_table = template

    def create_Oedge_table(self):
        cc = CubieCube()
        template = [[-1] * 18 for _ in range(self.NO_Oedge_coords)]

        for coord in range(self.NO_Oedge_coords):
            for i, move in enumerate(self.moves):
                cc.o_edge_coords = coord
                for power in range(3):
                    cc.edge_orientation_move(move)
                    template[coord][(3 * i) + power] = cc.o_edge_coords

        self.Oedge_table = template

    def create_POSud_slice_table(self):
        cc = CubieCube()
        template = [[-1] * 18 for _ in range(self.NO_POSud_slice_coords)]

        for coord in range(self.NO_POSud_slice_coords):
            for i, move in enumerate(self.moves):
                cc.pos_udslice_coords = coord
                for power in range(3):
                    cc.edge_permutation_move(move)
                    template[coord][(3 * i) + power] = cc.pos_udslice_coords

        self.POSud_slice_table = template

    # Phase 1 pruning tables
    def create_UDslice_Ocorner_Ptable(self):
        """
        Method to construct the pruning table for use in the heuristic that combines corner orientation and UD-slice 
        edge positioning. 
        """
        
        # Create a template that allows every corner orientation coordinate to intersect with every UD-slice edge 
        # position coordinate. 
        table = [[-1] * self.NO_Ocorner_coords for _ in range(self.NO_POSud_slice_coords)]
        # Set the root of the search.
        table[0][0] = 0
        # Every combination of corner orientation and UD-slice edge position can be reached within 11 moves from the 
        # root of the search. 
        for depth in range(10):
            # For every UD-slice edge position coordinate
            for UDslice_edge_position_coord, twist_coordinate_collection in enumerate(table):
                # For every corner orientation per UD-slice edge position coordinate
                for corner_orientation_coord, place in enumerate(twist_coordinate_collection):
                    # If the position is reachable at this depth, explore and mark all connecting positions.
                    if place == depth:
                        # For every move of the 18 as described in the move tables.
                        for move in range(18):
                            # Look up new corner orientation coordinate.
                            new_corner_orientation_coord = self.Ocorner_table[corner_orientation_coord][move]
                            # Look up new UD-slice edge position coordinate.
                            new_UDslice_edge_position_coord = self.POSud_slice_table[UDslice_edge_position_coord][move]
                            # If the new position after a move has not been explored in previous iterations of the 
                            # breadth first search. 
                            if table[new_UDslice_edge_position_coord][new_corner_orientation_coord] == -1:
                                # Mark for exploration in next iteration of search
                                table[new_UDslice_edge_position_coord][new_corner_orientation_coord] = depth + 1

        self.UDslice_Ocorner_pruning_table = table

    def create_UDslice_Oedge_Ptable(self):
        table = [[-1] * self.NO_Oedge_coords for _ in range(self.NO_POSud_slice_coords)]
        table[0][0] = 0

        for depth in range(9):
            for slice_row, combo_coords in enumerate(table):
                for twist_column, place in enumerate(combo_coords):
                    if place == depth:
                        for move in range(18):
                            slice = self.POSud_slice_table[slice_row][move]
                            twist = self.Oedge_table[twist_column][move]
                            if table[slice][twist] == -1:
                                table[slice][twist] = depth + 1

        self.UDslice_Oedge_pruning_table = table

    # Phase 2 move tables
    def create_Pcorner_table(self):
        cc = CubieCube()
        template = [[0] * 18 for _ in range(self.NO_Pcorner_coords)]
        # 1 is fine, 0 and 2 are not fine unless its a ud face

        for coord in range(self.NO_Pcorner_coords):
            for i, move in enumerate(self.moves):
                cc.p_corner_coords = coord
                for power in range(3):
                    cc.corner_permutation_move(move)
                    if power != 1 and i % 5 != 0:
                        template[coord][(3 * i) + power] = -1
                    else:
                        template[coord][(3 * i) + power] = cc.p_corner_coords

        self.Pcorner_table = template

    def create_P8edge_table(self):
        cc = CubieCube()
        template = [[0] * 18 for _ in range(self.NO_P8edge_coords)]
        # allow single turns of the up and down face, and double turns of everything else
        # for up and down face, anything will go - so move % 3 = 0
        # for other faces, power must be 1 or not at all
        for coord in range(self.NO_P8edge_coords):
            for i, move in enumerate(self.moves):
                cc.p_8edge_coords = coord
                for power in range(3):
                    cc.edge_permutation_move(move)
                    if power != 1 and i % 5 != 0:
                        template[coord][(3 * i) + power] = -1
                    else:
                        template[coord][(3 * i) + power] = cc.p_8edge_coords
        self.P8edge_table = template

    def create_P4edge_table(self):
        cc = CubieCube()
        template = [[0] * 18 for _ in range(self.NO_P4edge_coords)]
        # allow single turns of the up and down face, and double turns of everything else
        # for up and down face, anything will go - so move % 3 = 0
        # for other faces, power must be 1 or not at all
        for coord in range(self.NO_P4edge_coords):
            for i, move in enumerate(self.moves):
                cc.p_4edge_coords = coord
                for power in range(3):
                    cc.edge_permutation_move(move)
                    if power != 1 and i % 5 != 0:
                        template[coord][(3 * i) + power] = -1
                    else:
                        template[coord][(3 * i) + power] = cc.p_4edge_coords
        self.P4edge_table = template

    # Phase 2 pruning tables
    def create_P4edge_Pcorner_Ptable(self):
        table = [[-1] * self.NO_Pcorner_coords for _ in range(self.NO_P4edge_coords)]
        table[0][0] = 0
        for depth in range(14):
            for P4edge_row, combo_coords in enumerate(table):
                for Pcorner_column, place in enumerate(combo_coords):
                    if place == depth:
                        for move in range(18):
                            edge4 = self.P4edge_table[P4edge_row][move]
                            Pcorner = self.Pcorner_table[Pcorner_column][move]
                            if edge4 == -1 or Pcorner == -1:
                                continue
                            if table[edge4][Pcorner] == -1:
                                table[edge4][Pcorner] = depth + 1

        self.P4edge_Pcorner_Ptable = table

    def create_P4edge_P8edge_Ptable(self):  # Not working
        table = [[-1] * self.NO_P8edge_coords for _ in range(self.NO_P4edge_coords)]
        table[0][0] = 0
        for depth in range(13):
            for P4edge_row, combo_coords in enumerate(table):
                for P8edge_column, place in enumerate(combo_coords):
                    if place == depth:
                        for move in range(18):
                            edge4 = self.P4edge_table[P4edge_row][move]
                            edge8 = self.P8edge_table[P8edge_column][move]
                            if edge4 == -1 or edge8 == -1:
                                continue
                            if table[edge4][edge8] == -1:
                                table[edge4][edge8] = depth + 1

        self.P4edge_P8edge_Ptable = table
