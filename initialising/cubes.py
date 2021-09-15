from definitions.cubedefs import *
from functools import reduce
from math import comb as CNK
from misc.rotating import rotate_left


class facelet_cube:

    def __init__(self, string_definition=None):
        self.f = [0] * 54

        if string_definition:
            for i, c in enumerate(string_definition):
                self.f[i] = axes[c]

            self.verify()
            pass

        else:
            self.f = [-1] * 54

    def verify(self):
        # quantity of facelets
        count = [0] * len(axes)
        for i, c in enumerate(axes):
            count[i] = self.f.count(c)

        for c in count:
            if c != 9:
                return -1

    @property
    def corners(self):
        s = self.f
        corners = [0] * len(corner_indices)
        for i in range(len(corners)):
            corners[i] = tuple(s[f] for f in corner_facelet_indices[i])

        return corners

    @property
    def edges(self):
        s = self.f
        edges = [0] * len(edge_indices)
        for i in range(len(edges)):
            edges[i] = tuple(s[f] for f in edge_facelet_indices[i])

        return edges

    def to_cubeie_cube(self):

        # get the permutation of the corners

        co = [0] * 8
        cp = [0] * 8
        for i, corner in enumerate(self.corners):
            for o, f in enumerate(corner):
                if f == 0 or f == 5:
                    break

            f1 = corner[(o + 1) % 3]
            f2 = corner[(o + 2) % 3]

            for j, c in enumerate(corner_axes):
                if f1 == c[1] and f2 == c[2]:
                    co[i] = o
                    cp[i] = j
                    break

        eo = [0] * 12
        ep = [0] * 12

        for t, edge in enumerate(self.edges):
            for k, cols in enumerate(edge_axes):

                if edge == cols:
                    eo[t] = 0
                    ep[t] = k

                elif edge[0] == cols[1] and edge[1] == cols[0]:
                    eo[t] = 1
                    ep[t] = k

        cc = cubiecube(cp, co, ep, eo)

        return cc


class cubiecube:
    Ocorner_parity_value = [0, 2, 1]

    def __init__(self, cp=None, co=None, ep=None, eo=None):
        self.cp = cp if cp else list(range(0, 8))
        self.co = co if co else [0] * 8
        self.ep = ep if ep else list(range(0, 12))
        self.eo = eo if eo else [0] * 12

    def to_coord_cube(self):

        cc = coord_cube(self.Pcorner_coords, self.Ocorner_coords, self.Pedge_coords, self.Oedge_coords)

        return cc

    def to_facelet_cube(self):
        fc = facelet_cube()

        for corner in corner_indices:
            for f in range(3):
                fc.f[corner_facelet_indices[corner][(self.co[corner] + f) % 3]] = corner_axes[self.cp[corner]][f]

        for edge in edge_indices:
            for e in range(2):
                fc.f[edge_facelet_indices[edge][(self.eo[edge] + e) % 2]] = edge_axes[self.ep[edge]][e]

        fc.f = [facelet_to_col[col] if col != -1 else facelet_to_col[i // 9] for i, col in enumerate(fc.f)]

        return "".join(fc.f)

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
    def Ocorner_coords(self):  # working
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
    def Pcorner_coords(self, index):  # working
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

    # The following are used under the assumption
    # that the UD slice edges are in the ud slice prior to use.
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


class coord_cube:
    def __init__(self, cp=None, co=None, ep=None, eo=None):
        self.cp = cp if cp else 0
        self.co = co if co else 0
        self.ep = ep if ep else 0
        self.eo = eo if eo else 0

    def return_coords(self):
        return [self.cp, self.co, self.ep, self.co]
