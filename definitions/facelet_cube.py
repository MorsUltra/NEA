# Import all the default pieces.
from definitions.cubedefs import *
from definitions.cubie_cube import CubieCube


class Facelet_Cube:
    """
    Lowest level of data structure involved in Two-Phase Algorithm. It deals primarily in colours and operates on the
    basis of stickers or "facelets".
    """

    def __init__(self, string_definition: str = None):
        """
        Constructor for FaceletCube.

        :param string_definition: definition of a cube in facelet string form.
        """

        self.f: list[int] = [0] * 54

        if string_definition:
            for i, c in enumerate(string_definition):
                self.f[i] = Axes[c]

        else:
            self.f = [-1] * 54

    def verify(self) -> int:
        """
        Function to determine the validity of a cube defined as a string.

        :return: -1 if not a valid string; 1 if a valid string.
        """

        # Count the frequency of each value.
        count: list[0] = [0] * len(Axes)
        for i, c in enumerate(Axes):
            count[i] = self.f.count(c)

        for c in count:
            # If there are not 9 colours of each facelet.
            if c != 9:
                return -1

        return 1

    @property
    def corners(self) -> list[tuple[int, int, int]]:
        """
        Getter method for the corners of the string definition of a cube.

        :return: A list of corners pulled from positions in the string definition of a cube.
        """

        s = self.f
        corner_facelets = [0] * len(Corner_Indices)
        # Loop through the corners.
        for i in range(len(corner_facelets)):
            corner_facelets[i] = tuple(s[f] for f in corner_facelet_indices[i])

        return corner_facelets

    @property
    def edges(self) -> list[tuple[int, int, int]]:
        """
        Getter method for the edges of the string definition of a cube.

        :return: A list of edges pulled from positions in the string definition of a cube.
        """

        s = self.f
        edges = [0] * len(Edge_Indices)
        # Loop through the edges.
        for i in range(len(edges)):
            edges[i] = tuple(s[f] for f in edge_facelet_indices[i])

        return edges

    def to_cubie_cube(self, cc: CubieCube):
        """
        Function to convert FaceletCube into CubieCube

        :param cc: clean CubieCube object to use in conversion of string definition.
        :return: CubieCube with facelet string definition applied.
        """

        # Create empty lists
        co = [0] * 8
        cp = [0] * 8

        # Loop through the corners in the current facelet string.
        for i, corner in enumerate(self.corners):
            # Loop through the individual facelets.
            for o, f in enumerate(corner):
                # If the facelet is either a part of the top (0) or down (5) face.
                if f == 0 or f == 5:
                    # Break loop as orientation has been determined.
                    break

            # Loop through the facelets remaining in that corner, starting from the up or down facelet and moving
            # clockwise
            facelet1 = corner[(o + 1) % 3]
            facelet2 = corner[(o + 2) % 3]

            # For the corners that exist on a cube
            for j, default_corner in enumerate(corner_axes):
                # If two of the facelets match in corner in order, then it must be that corner and cannot be another
                # assuming all inputs have been sanitised.
                if facelet1 == default_corner[1] and facelet2 == default_corner[2]:
                    co[i] = o
                    cp[i] = j
                    break

        # Create empty lists
        eo = [0] * 12
        ep = [0] * 12

        # Loop through the corners in the current facelet string.
        for t, edge in enumerate(self.edges):
            # Loop through the default edges.
            for k, cols in enumerate(edge_axes):
                # If the edge taken from string definition matches default edge with no flip.
                if edge == cols:
                    eo[t] = 0
                    ep[t] = k

                # If the edge taken from string definition matches default edge with flip.
                elif edge[0] == cols[1] and edge[1] == cols[0]:
                    eo[t] = 1
                    ep[t] = k

        cc.cp = cp
        cc.co = co
        cc.ep = ep
        cc.eo = eo

        return cc
