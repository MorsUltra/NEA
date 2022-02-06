from definitions.cubedefs import *


class Facelet_Cube:

    def __init__(self, string_definition=None):
        self.f = [0] * 54

        if string_definition:
            for i, c in enumerate(string_definition):
                self.f[i] = Axes[c]

            self.verify()
            pass

        else:
            self.f = [-1] * 54

    def verify(self):
        count = [0] * len(Axes)
        for i, c in enumerate(Axes):
            count[i] = self.f.count(c)

        for c in count:
            if c != 9:
                return -1

    @property
    def corners(self):
        s = self.f
        corners = [0] * len(Corner_Indices)
        for i in range(len(corners)):
            corners[i] = tuple(s[f] for f in corner_facelet_indices[i])

        return corners

    @property
    def edges(self):
        s = self.f
        edges = [0] * len(Edge_Indices)
        for i in range(len(edges)):
            edges[i] = tuple(s[f] for f in edge_facelet_indices[i])

        return edges

    def to_cubeie_cube(self, cc):
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

        cc.cp = cp
        cc.co = co
        cc.ep = ep
        cc.eo = eo

        return cc
