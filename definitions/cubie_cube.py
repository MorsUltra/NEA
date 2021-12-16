from functools import reduce
from math import comb as CNK
from random import randint

from definitions.cubedefs import *


class cubiecube:
    MOVES = []

    Ocorner_parity_value = [0, 2, 1]

    def __init__(self, cp: list = None, co: list = None, ep: list = None, eo: list = None, moves=None):
        self.cp = cp if cp else list(range(0, 8))
        self.co = co if co else [0] * 8
        self.ep = ep if ep else list(range(0, 12))  # TODO not sure if you need the list
        self.eo = eo if eo else [0] * 12

        if moves:
            self.MOVE_arr(*moves)

    def to_data_arr(self) -> tuple[list | list, list | list[int], list | list, list | list[int]]:
        return self.cp, self.co, self.ep, self.eo

    def to_facelet_cube(self, fc) -> str:
        for corner in corner_indices:
            for f in range(3):
                fc.f[corner_facelet_indices[corner][(self.co[corner] + f) % 3]] = corner_axes[self.cp[corner]][f]

        for edge in edge_indices:
            for e in range(2):
                fc.f[edge_facelet_indices[edge][(self.eo[edge] + e) % 2]] = edge_axes[self.ep[edge]][e]

        fc.f = [facelet_to_col[col] if col != -1 else facelet_to_col[i // 9] for i, col in enumerate(fc.f)]

        return "".join(fc.f)

    def shuffle(self):
        self.Ocorner_coords = randint(0, 2186)
        self.Oedge_coords = randint(0, 2047)
        while True:
            self.Pcorner_coords = randint(0, 40319)
            self.Pedge_coords = randint(0, 479001599)
            if self.edge_parity != self.corner_parity:
                continue
            else:
                break

    def MOVE_arr(self, moves, powers):
        for i, move in enumerate(moves):
            for power in range(powers[i]):
                self.MOVE(MOVES[move])

    def MOVE(self, to_apply):
        self.Cmove(to_apply)
        self.Emove(to_apply)

    def Cmove(self, to_apply):
        self.cp = [self.cp[to_apply.cp[i]] for i in range(8)]
        self.co = [(self.co[to_apply.cp[i]] + to_apply.co[i]) % 3 for i in range(8)]

    def Emove(self, to_apply):
        self.ep = [self.ep[to_apply.ep[i]] for i in range(12)]
        self.eo = [(self.eo[to_apply.ep[i]] + to_apply.eo[i]) % 2 for i in range(12)]

    @property
    def corner_parity(self) -> int:
        parity = 0
        for q in range(7, 0, -1):
            for corner in self.cp[:q]:
                if corner > self.cp[q]:
                    parity += 1
        return parity % 2

    @property
    def edge_parity(self) -> int:
        parity = 0
        for q in range(11, 0, -1):
            for edge in self.ep[:q]:
                if edge > self.ep[q]:
                    parity += 1

        return parity % 2

    @property
    def Ocorner_coords(self):
        co = reduce(lambda variable_base, total: 3 * variable_base + total, self.co[:7])

        return co

    @Ocorner_coords.setter
    def Ocorner_coords(self, index):  # working
        parity = 0
        self.co = [-1] * 8
        for _ in range(6, -1, -1):
            parity += index % 3
            self.co[_] = index % 3
            index //= 3

        parity %= 3
        parity = self.Ocorner_parity_value[parity]
        self.co[-1] = parity

    @property
    def Pcorner_coords(self):  # working
        index = 0
        # Fairly confident this is working. Not the problem
        for p in range(7, 0, -1):
            higher = 0
            for corner in self.cp[:p]:
                if corner > self.cp[p]:
                    higher += 1

            index = (index + higher) * p

        return index

    @Pcorner_coords.setter
    def Pcorner_coords(self, index):
        corners = list(range(8))
        self.cp = [-1] * 8
        coeffs = [0] * 7
        for i in range(2, 9):
            coeffs[i - 2] = index % i
            index //= i

        for i in range(7, 0, -1):
            self.cp[i] = corners.pop(i - coeffs[i - 1])

        self.cp[0] = corners[0]

    @property
    def Oedge_coords(self):  # working
        eo = reduce(lambda variable_base, total: 2 * variable_base + total, self.eo[:11])

        return eo

    @Oedge_coords.setter
    def Oedge_coords(self, index):  # working
        parity = 0
        self.eo = [-1] * 12
        for _ in range(10, -1, -1):
            parity += index % 2
            self.eo[_] = index % 2
            index //= 2

        self.eo[-1] = parity % 2

    @property
    def Pedge_coords(self):  # working
        ep = 0

        for p in range(11, 0, -1):
            higher = 0
            for edge in self.ep[:p]:
                if edge > self.ep[p]:
                    higher += 1

            ep = (ep + higher) * p

        return ep

    @Pedge_coords.setter
    def Pedge_coords(self, index):  # working
        corners = list(range(12))
        self.ep = [-1] * 12
        coeffs = [0] * 11
        for i in range(2, 13):
            coeffs[i - 2] = index % i
            index //= i

        for i in range(11, 0, -1):
            self.ep[i] = corners.pop(i - coeffs[i - 1])

        self.ep[0] = corners[0]

    # ---------------------------------------------------------

    @property
    def P8edge_coords(self):
        coord = 0

        for p in range(7, 0, -1):
            higher = 0
            for edge in self.ep[:p]:
                if edge > self.ep[p]:
                    higher += 1

            coord = (coord + higher) * p

        return coord

    @P8edge_coords.setter
    def P8edge_coords(self, index):
        corners = list(range(8))
        self.ep[:8] = [-1] * 8
        coeffs = [0] * 7
        for i in range(2, 9):
            coeffs[i - 2] = index % i
            index //= i

        for i in range(7, 0, -1):
            self.ep[i] = corners.pop(i - coeffs[i - 1])

        self.ep[0] = corners[0]

    @property
    def P4edge_coords(self):
        cord = 0
        ep = self.ep[8:]
        for p in range(3, 0, -1):
            higher = 0
            for edge in ep[:p]:
                if edge > ep[p]:
                    higher += 1

            cord = (cord + higher) * p

        return cord

    @P4edge_coords.setter
    def P4edge_coords(self, index):
        self.ep[8:] = [-1] * 4

        corners = list(range(8, 12))
        coeffs = [0] * 3
        for i in range(2, 5):
            coeffs[i - 2] = index % i
            index //= i

        for i in range(3, 0, -1):
            self.ep[8 + i] = corners.pop(i - coeffs[i - 1])

        self.ep[8] = corners[0]

    @property
    def POSud_slice_coords(self):  # working
        blank = [False] * 12
        for i, corner in enumerate(self.ep):
            if corner >= 8:
                blank[i] = True

        coord = 0
        count = 3

        for i in range(11, -1, -1):
            if count < 0:
                break

            if blank[i]:
                count -= 1
            else:
                coord += CNK(i, count)

        return coord

    @POSud_slice_coords.setter
    def POSud_slice_coords(self, index):  # working
        count = 3
        self.ep = [False] * 12

        for i in range(11, -1, -1):
            if count < 0:
                break

            v = CNK(i, count)

            if index < v:
                # noinspection PyTypeChecker
                self.ep[i] = 8 + count
                count -= 1
            else:
                index -= v

        others = 0
        for i, edge in enumerate(self.ep):
            if not edge:
                # noinspection PyTypeChecker
                self.ep[i] = others
                others += 1


cpU = [corner_indices.UBR, corner_indices.URF, corner_indices.UFL, corner_indices.ULB, corner_indices.DFR,
       corner_indices.DLF, corner_indices.DBL, corner_indices.DRB]
coU = [0, 0, 0, 0, 0, 0, 0, 0]
epU = [edge_indices.UB, edge_indices.UR, edge_indices.UF, edge_indices.UL, edge_indices.DR, edge_indices.DF,
       edge_indices.DL, edge_indices.DB, edge_indices.FR, edge_indices.FL, edge_indices.BL, edge_indices.BR]
eoU = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cpR = [corner_indices.DFR, corner_indices.UFL, corner_indices.ULB, corner_indices.URF, corner_indices.DRB,
       corner_indices.DLF, corner_indices.DBL, corner_indices.UBR]
coR = [2, 0, 0, 1, 1, 0, 0, 2]
epR = [edge_indices.FR, edge_indices.UF, edge_indices.UL, edge_indices.UB, edge_indices.BR, edge_indices.DF,
       edge_indices.DL, edge_indices.DB, edge_indices.DR, edge_indices.FL, edge_indices.BL, edge_indices.UR]
eoR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cpF = [corner_indices.UFL, corner_indices.DLF, corner_indices.ULB, corner_indices.UBR, corner_indices.URF,
       corner_indices.DFR, corner_indices.DBL, corner_indices.DRB]
coF = [1, 2, 0, 0, 2, 1, 0, 0]
epF = [edge_indices.UR, edge_indices.FL, edge_indices.UL, edge_indices.UB, edge_indices.DR, edge_indices.FR,
       edge_indices.DL, edge_indices.DB, edge_indices.UF, edge_indices.DF, edge_indices.BL, edge_indices.BR]
eoF = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

cpD = [corner_indices.URF, corner_indices.UFL, corner_indices.ULB, corner_indices.UBR, corner_indices.DLF,
       corner_indices.DBL, corner_indices.DRB, corner_indices.DFR]
coD = [0, 0, 0, 0, 0, 0, 0, 0]
epD = [edge_indices.UR, edge_indices.UF, edge_indices.UL, edge_indices.UB, edge_indices.DF, edge_indices.DL,
       edge_indices.DB, edge_indices.DR, edge_indices.FR, edge_indices.FL, edge_indices.BL, edge_indices.BR]
eoD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cpL = [corner_indices.URF, corner_indices.ULB, corner_indices.DBL, corner_indices.UBR, corner_indices.DFR,
       corner_indices.UFL, corner_indices.DLF, corner_indices.DRB]
coL = [0, 1, 2, 0, 0, 2, 1, 0]
epL = [edge_indices.UR, edge_indices.UF, edge_indices.BL, edge_indices.UB, edge_indices.DR, edge_indices.DF,
       edge_indices.FL, edge_indices.DB, edge_indices.FR, edge_indices.UL, edge_indices.DL, edge_indices.BR]
eoL = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cpB = [corner_indices.URF, corner_indices.UFL, corner_indices.UBR, corner_indices.DRB, corner_indices.DFR,
       corner_indices.DLF, corner_indices.ULB, corner_indices.DBL]
coB = [0, 0, 1, 2, 0, 0, 2, 1]
epB = [edge_indices.UR, edge_indices.UF, edge_indices.UL, edge_indices.BR, edge_indices.DR, edge_indices.DF,
       edge_indices.DL, edge_indices.BL, edge_indices.FR, edge_indices.FL, edge_indices.UB, edge_indices.DB]
eoB = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]

Umove = cubiecube(cp=cpU, co=coU, ep=epU, eo=eoU)
Rmove = cubiecube(cp=cpR, co=coR, ep=epR, eo=eoR)
Lmove = cubiecube(cp=cpL, co=coL, ep=epL, eo=eoL)
Fmove = cubiecube(cp=cpF, co=coF, ep=epF, eo=eoF)
Bmove = cubiecube(cp=cpB, co=coB, ep=epB, eo=eoB)
Dmove = cubiecube(cp=cpD, co=coD, ep=epD, eo=eoD)

MOVES = [Umove,
         Rmove,
         Lmove,
         Fmove,
         Bmove,
         Dmove]
cubiecube.moves = MOVES
