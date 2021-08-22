from definitions.cubedefs import  *
from pprint import pprint
from definitions.defaults import *

class facelet_cube:

    def __init__(self, string_definition="UUUUUUUUURRRRRRRRRLLLLLLLLLFFFFFFFFFBBBBBBBBBDDDDDDDDD"):
        self.f = [0] * len(string_definition)
        for i, c in enumerate(string_definition):
            self.f[i] = colours[c]

        self.verify()

    def verify(self):
        # quantity of facelets
        count = [0] * len(colours)
        for i, c in enumerate(colours):
            count[i] = self.f.count(c)

        for c in count:
            if c != 9:
                return -1


    @property
    def corners(self):
        s = self.f
        corners = [0] * len(corner_index)
        for i in range(len(corners)):
            corners[i] = tuple(s[f] for f in corner_facelet_index[i])

        return corners

    @property
    def edges(self):
        s = self.f
        edges = [0] * len(edge_index)
        for i in range(len(edges)):
            edges[i] = tuple(s[f] for f in edge_facelet_index[i])

        return edges

    def cubiecube_setup(self):


        # get the permutation of the corners

        co = [0] * 8
        cp = [0] * 8
        for i, corner in enumerate(self.corners):
            for o, f in enumerate(corner):
                if f == 0 or f == 5:
                    break

            f1 = corner[(o + 1) % 3]
            f2 = corner[(o + 2) % 3]

            for j, c in enumerate(corner_colours):
                if f1 == c[1] and f2 == c[2]:
                    co[i] = o
                    cp[i] = j
                    break


        eo = [0] * 12
        ep = [0] * 12

        for t, edge in enumerate(self.edges):
            for k, cols in enumerate(edge_colours):

                if edge == cols:
                    eo[t] = 0
                    ep[t] = k

                elif edge[0] == cols[1] and edge[1] == cols[0]:
                    eo[t] = 1
                    ep[t] = k

        return co, cp, eo, ep


class cubiecube:
    def __init__(self, cp=None, co=None, ep=None, eo=None):
        self.cp = cp if cp else list(range(0, 8))
        self.co = co if co else [0] * 8
        self.ep = ep if ep else list(range(0, 12))
        self.eo = eo if eo else [0] * 12



# TODO impliment same system for edges, and orientation of corners too. Just a bunch of "if's"

string_def = "UUU UUU UUR FRR RRR RRR LLL LLL LLL FFU FFF FFF BBB BBB BBB DDD DDD DDD"
string_def = "RFD LUD DUF LRR RRB RDR FFL BLD UBL BFU LFU FDB FRU UBR BLB DBU LDF LUD"
string_def = string_def.replace(" ", "")


print(string_def)
f = facelet_cube(string_def)
pprint(f.cubiecube_setup())

# from GUI import vis
#
# vis.print_cube(string_def)