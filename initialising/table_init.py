from definitions.moves import *
import numpy as np
import os


class tables:
    NO_Ocorner_coords = 2187
    NO_Pcorner_coords = 40320

    NO_Oedge_coords = 2048

    NO_POSud_slice_coords = 495

    NO_P4edge_coords = 24
    NO_P8edge_coords = 40320

    moves = [Umove,
             Rmove,
             Lmove,
             Dmove,
             Fmove,
             Bmove]

    save_file_name = r"\Pruning tables.npz"

    def __init__(self, load=True, save=True):
        table_file_path = os.getcwd() + self.save_file_name

        self.Ocorner_table = []
        self.Pcorner_table = []
        self.Oedge_table = []
        self.POSud_slice_table = []
        self.P4edge_table = []
        self.P8edge_table = []

        # Pruning tables

        self.UDslice_Oedge_pruning_table = []
        self.UDslice_Ocorner_pruning_table = []

        self.P4edge_P8edge_Ptable = []
        self.P4edge_Pcorner_Ptable = []

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
        self.create_Ocorner_table()  # This is working fine
        self.create_Pcorner_table()  # This is working fine
        self.create_Oedge_table()  # This is working fine
        self.create_POSud_slice_table()  # This is working fine
        self.create_UDslice_Ocorner_Ptable()  # This is working fine
        self.create_UDslice_Oedge_Ptable()  # This is working fine

        self.create_P4edge_table()  # This is working fine
        self.create_P8edge_table()  # This is working fine
        self.create_P4edge_P8edge_Ptable()  # This MIGHT be working fine, however indexing seems to be different
        self.create_P4edge_Pcorner_Ptable()  # This MIGHT be working fine, however indexing seems to be different

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

    def create_UDslice_Ocorner_Ptable(self):
        table = [[-1] * self.NO_Ocorner_coords for _ in range(self.NO_POSud_slice_coords)]
        table[0][0] = 0
        for depth in range(9):
            for slice_row, combo_coords in enumerate(table):
                for twist_column, place in enumerate(combo_coords):
                    if place == depth:
                        for move in range(18):
                            twist = self.Ocorner_table[twist_column][move]
                            slice = self.POSud_slice_table[slice_row][move]
                            if table[slice][twist] == -1:
                                table[slice][twist] = depth + 1

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

    def create_P4edge_P8edge_Ptable(self):
        table = [[-1] * self.NO_P8edge_coords for _ in range(self.NO_P4edge_coords)]
        table[0][0] = 0
        for depth in range(12):
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


    def create_POSud_slice_table(self):
        cc = cubiecube()
        template = [[-1] * 18 for _ in range(self.NO_POSud_slice_coords)]

        for coord in range(self.NO_POSud_slice_coords):
            for i, move in enumerate(self.moves):
                cc.POSud_slice_coords = coord
                for power in range(3):
                    cc.Emove(move)
                    template[coord][(3 * i) + power] = cc.POSud_slice_coords

        self.POSud_slice_table = template

    def create_Oedge_table(self):
        cc = cubiecube()
        template = [[-1] * 18 for _ in range(self.NO_Oedge_coords)]

        for coord in range(self.NO_Oedge_coords):
            for i, move in enumerate(self.moves):
                cc.Oedge_coords = coord
                for power in range(3):
                    cc.Emove(move)
                    template[coord][(3 * i) + power] = cc.Oedge_coords

        self.Oedge_table = template

    def create_Pcorner_table(self):
        cc = cubiecube()
        template = [[-1] * 18 for _ in range(self.NO_Pcorner_coords)]
        # 1 is fine, 0 and 2 are not fine unless its a ud face

        for coord in range(self.NO_Pcorner_coords):
            for i, move in enumerate(self.moves):
                cc.Pcorner_coords = coord
                for power in range(3):
                    cc.Cmove(move)
                    if power != 1 and i % 3 != 0:
                        continue
                    else:
                        template[coord][(3 * i) + power] = cc.Pcorner_coords

        self.Pcorner_table = template

    def create_Ocorner_table(self):
        cc = cubiecube()
        template = [[-1] * 18 for _ in range(self.NO_Ocorner_coords)]

        for coord in range(self.NO_Ocorner_coords):  # for every possible orientation of the corners
            for i, move in enumerate(self.moves):  # apply every move
                cc.Ocorner_coords = coord
                for power in range(3):  # for every turn possible
                    cc.Cmove(move)
                    template[coord][(3 * i) + power] = cc.Ocorner_coords

        self.Ocorner_table = template

    def create_P4edge_table(self):
        cc = cubiecube()
        template = [[-1] * 18 for _ in range(self.NO_P4edge_coords)]
        # allow single turns of the up and down face, and double turns of everything else
        # for up and down face, anything will go - so move % 3 = 0
        # for other faces, power must be 1 or not at all
        for coord in range(self.NO_P4edge_coords):
            for i, move in enumerate(self.moves):
                cc.P4edge_coords = coord
                for power in range(3):
                    cc.Emove(move)
                    if power != 1 and i % 3 != 0:
                        continue
                    else:
                        template[coord][(3 * i) + power] = cc.P4edge_coords
        self.P4edge_table = template

    def create_P8edge_table(self):
        cc = cubiecube()
        template = [[-1] * 18 for _ in range(self.NO_P8edge_coords)]
        # allow single turns of the up and down face, and double turns of everything else
        # for up and down face, anything will go - so move % 3 = 0
        # for other faces, power must be 1 or not at all
        for coord in range(self.NO_P8edge_coords):
            for i, move in enumerate(self.moves):
                cc.P8edge_coords = coord
                for power in range(3):
                    cc.Emove(move)
                    if power != 1 and i % 3 != 0:
                        continue
                    else:
                        template[coord][(3 * i) + power] = cc.P8edge_coords
        self.P8edge_table = template
