from functools import reduce
from math import comb as CNK
from random import randint

from definitions.cubedefs import *


class CubieCube:
    MOVES = []

    Ocorner_parity_value = [0, 2, 1]

    def __init__(self, data=None, moves=None):
        self.cp = data[0] if data else list(range(0, 8))
        self.co = data[1] if data else [0] * 8
        self.ep = data[2] if data else list(range(0, 12))  # TODO not sure if you need the list
        self.eo = data[3] if data else [0] * 12

        if moves:
            self.MOVE_arr(*moves)

    def is_solved(self):
        if self.to_data_arr() == (
                [0, 1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
            return True
        else:
            return False

    def verify(self):
        if self.edge_parity != self.corner_parity:
            return -1
        else:
            return 1

    def to_data_arr(self):
        return self.cp, self.co, self.ep, self.eo

    def to_facelet_string(self, fc) -> str:
        for corner in Corner_Indices:
            for f in range(3):
                fc.f[corner_facelet_indices[corner][(self.co[corner] + f) % 3]] = corner_axes[self.cp[corner]][f]

        for edge in Edge_Indices:
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
                # print(self.Pcorner_coords, self.Ocorner_coords, self.Pedge_coords, self.Oedge_coords)
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

    def COmove(self, to_apply):
        self.co = [(self.co[to_apply.cp[i]] + to_apply.co[i]) % 3 for i in range(8)]

    def CPmove(self, to_apply):
        self.cp = [self.cp[to_apply.cp[i]] for i in range(8)]

    def Emove(self, to_apply):
        self.ep = [self.ep[to_apply.ep[i]] for i in range(12)]
        self.eo = [(self.eo[to_apply.ep[i]] + to_apply.eo[i]) % 2 for i in range(12)]

    def EOmove(self, to_apply):
        self.eo = [(self.eo[to_apply.ep[i]] + to_apply.eo[i]) % 2 for i in range(12)]

    def EPmove(self, to_apply):
        self.ep = [self.ep[to_apply.ep[i]] for i in range(12)]

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
    def Ocorner_coords(self) -> int:
        """
        Getter function for corner orientation coordinate.
        
        :return: A ternary number from 0 --> 2186 (3^7 - 1).
        """

        co = reduce(lambda variable_base, total: 3 * variable_base + total, self.co[:7])

        return co

    @Ocorner_coords.setter
    def Ocorner_coords(self, index: int):
        """
        Setter function for corner orientation coordinates. Takes an index and changes the cube's corner orientation
        to reflect that coordinate.

        :param index: index of corner orientation to change to.
        """

        self.co = [0] * 8
        # Loop through the 7 most significant bits, leaving the last to be implied.
        for i in range(6, -1, -1):
            # Collect the bit at index i which has significance 3^i; the remainder when divided by 3^i.
            self.co[i] = index % 3
            # Move to the next bit.
            index //= 3

        # Set the least significant bit by finding the bit required to make the sum a multiple of 3.
        self.co[7] = self.Ocorner_parity_value[sum(self.co) % 3]

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
    def Oedge_coords(self, index: int):
        """
        Algorithm to produce binary number of index range 2047 (2^11 - 1).

        :param index: Index of target edge orientation coordinate.
        """

        self.eo = [0] * 12
        for i in range(10, -1, -1):
            self.eo[i] = index % 2
            index //= 2

        self.eo[11] = sum(self.eo) % 2

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
    def POSud_slice_coords(self):
        """
        Algorithm to get the UD-slice coordinate of the current edge permutation.

        :return: UD-slice coordinate of the current cube.
        """

        # Set the running total of the coordinate.
        coordinate = 0
        # Set the number of UD-slice edges to find.
        pieces_remaining = 4

        # Loop backwards through the list.
        for i in range(11, -1, -1):
            # If there are no more pieces left to find.
            if not pieces_remaining:
                break

            # If a piece is a UD-slice edge.
            if self.ep[i] >= 8:
                # Decrease count.
                pieces_remaining -= 1
            else:
                # Add to running total the number of combinations that do not have a piece here.
                coordinate += CNK(i, pieces_remaining - 1)

        return coordinate

    @POSud_slice_coords.setter
    def POSud_slice_coords(self, index: int):
        """
        Algorithm to set the position of the UD-slice coordinate from index 0-494.

        :param index: index to change cube to # TODO this thing here needs completing I'm bored.
        """

        # Set the number of UD-slices to be placed.
        pieces_remaining = 4
        # Clean the edge permutation array.
        self.ep = [False] * 12
        # Other edges (8) so they can be filled into blanks.
        other_edges = 0

        # Loop through the edge array backwards.
        for i in range(11, -1, -1):
            # If there are no pieces left to place.
            if not pieces_remaining:
                # Fill in the other edges if some have yet to have been checked.
                for unchecked in range(i + 1):
                    self.ep[unchecked] = other_edges
                    other_edges += 1
                break

            # Find the number of combinations of the remaining pieces that have a piece at position i.
            possible_combinations = CNK(i, pieces_remaining - 1)

            # If the index is a part of one of those combinations.
            if index < possible_combinations:
                # Mark the position i to have a UD-slice edge placed there.
                self.ep[i] = 7 + pieces_remaining
                pieces_remaining -= 1
            else:
                # Eliminate those combinations from consideration.
                index -= possible_combinations
                # Fill in with non-UD-slice edge.
                self.ep[i] = other_edges
                other_edges += 1


cpU = [Corner_Indices.UBR, Corner_Indices.URF, Corner_Indices.UFL, Corner_Indices.ULB, Corner_Indices.DFR,
       Corner_Indices.DLF, Corner_Indices.DBL, Corner_Indices.DRB]
coU = [0, 0, 0, 0, 0, 0, 0, 0]
epU = [Edge_Indices.UB, Edge_Indices.UR, Edge_Indices.UF, Edge_Indices.UL, Edge_Indices.DR, Edge_Indices.DF,
       Edge_Indices.DL, Edge_Indices.DB, Edge_Indices.FR, Edge_Indices.FL, Edge_Indices.BL, Edge_Indices.BR]
eoU = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cpR = [Corner_Indices.DFR, Corner_Indices.UFL, Corner_Indices.ULB, Corner_Indices.URF, Corner_Indices.DRB,
       Corner_Indices.DLF, Corner_Indices.DBL, Corner_Indices.UBR]
coR = [2, 0, 0, 1, 1, 0, 0, 2]
epR = [Edge_Indices.FR, Edge_Indices.UF, Edge_Indices.UL, Edge_Indices.UB, Edge_Indices.BR, Edge_Indices.DF,
       Edge_Indices.DL, Edge_Indices.DB, Edge_Indices.DR, Edge_Indices.FL, Edge_Indices.BL, Edge_Indices.UR]
eoR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cpF = [Corner_Indices.UFL, Corner_Indices.DLF, Corner_Indices.ULB, Corner_Indices.UBR, Corner_Indices.URF,
       Corner_Indices.DFR, Corner_Indices.DBL, Corner_Indices.DRB]
coF = [1, 2, 0, 0, 2, 1, 0, 0]
epF = [Edge_Indices.UR, Edge_Indices.FL, Edge_Indices.UL, Edge_Indices.UB, Edge_Indices.DR, Edge_Indices.FR,
       Edge_Indices.DL, Edge_Indices.DB, Edge_Indices.UF, Edge_Indices.DF, Edge_Indices.BL, Edge_Indices.BR]
eoF = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

cpD = [Corner_Indices.URF, Corner_Indices.UFL, Corner_Indices.ULB, Corner_Indices.UBR, Corner_Indices.DLF,
       Corner_Indices.DBL, Corner_Indices.DRB, Corner_Indices.DFR]
coD = [0, 0, 0, 0, 0, 0, 0, 0]
epD = [Edge_Indices.UR, Edge_Indices.UF, Edge_Indices.UL, Edge_Indices.UB, Edge_Indices.DF, Edge_Indices.DL,
       Edge_Indices.DB, Edge_Indices.DR, Edge_Indices.FR, Edge_Indices.FL, Edge_Indices.BL, Edge_Indices.BR]
eoD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cpL = [Corner_Indices.URF, Corner_Indices.ULB, Corner_Indices.DBL, Corner_Indices.UBR, Corner_Indices.DFR,
       Corner_Indices.UFL, Corner_Indices.DLF, Corner_Indices.DRB]
coL = [0, 1, 2, 0, 0, 2, 1, 0]
epL = [Edge_Indices.UR, Edge_Indices.UF, Edge_Indices.BL, Edge_Indices.UB, Edge_Indices.DR, Edge_Indices.DF,
       Edge_Indices.FL, Edge_Indices.DB, Edge_Indices.FR, Edge_Indices.UL, Edge_Indices.DL, Edge_Indices.BR]
eoL = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cpB = [Corner_Indices.URF, Corner_Indices.UFL, Corner_Indices.UBR, Corner_Indices.DRB, Corner_Indices.DFR,
       Corner_Indices.DLF, Corner_Indices.ULB, Corner_Indices.DBL]
coB = [0, 0, 1, 2, 0, 0, 2, 1]
epB = [Edge_Indices.UR, Edge_Indices.UF, Edge_Indices.UL, Edge_Indices.BR, Edge_Indices.DR, Edge_Indices.DF,
       Edge_Indices.DL, Edge_Indices.BL, Edge_Indices.FR, Edge_Indices.FL, Edge_Indices.UB, Edge_Indices.DB]
eoB = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]

Umove = CubieCube(data=[cpU, coU, epU, eoU])
Rmove = CubieCube(data=[cpR, coR, epR, eoR])
Lmove = CubieCube(data=[cpL, coL, epL, eoL])
Fmove = CubieCube(data=[cpF, coF, epF, eoF])
Bmove = CubieCube(data=[cpB, coB, epB, eoB])
Dmove = CubieCube(data=[cpD, coD, epD, eoD])

MOVES = [Umove,
         Rmove,
         Lmove,
         Fmove,
         Bmove,
         Dmove]

CubieCube.moves = MOVES
