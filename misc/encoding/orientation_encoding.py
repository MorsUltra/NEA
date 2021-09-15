# There are 2186 possible ways to orientate the corners on a Rubik's Cube (3^7 - 1).
# NOTE: The first 7 corners determine the orientation of the last, hence 3^7 (sum(orientations)%3 = 0).
# The orientation of all the corners can be encoded using the ternary number system.
# Each corner has a rotation o, o ∈ {0, 1, 2}.
# EXAMPLE: The corner orientation 0012100(2) -> 144.
# The inverse can be applied to obtain the orientation of all the corners given it's index number.


class C:
    """
    Abstract Corner class.
    :cvar Cparity: the resultant value appended to orientation to make sum(orientations)%3 = 0
    """

    Cparity: dict[int, int] = {
        0: 0,
        1: 2,
        2: 1
    }

    @staticmethod
    def get_index(orientation: int) -> int:
        """
        Get index number of corner orientation.
        
        :speed_test timeit("C.get_index(20011002)", setup="from file import C"): 0.3337274000000008
        :param orientation: orientation of corners.
        :return: index number of given orientation.
        """

        return int(str(orientation)[:-1], 3)

    @staticmethod
    def get_orientation(index: int) -> int:
        """
        Get orientation of corners of given index.
        
        :speed_test timeit("C.get_orientation(1494)", setup="from file import C"): 2.1323447999999985
        :param index: index number to be converted.
        :return: orientation of given index.
        """

        parity = 0
        ori = ""
        for _ in range(7):
            parity += (index % 3)
            ori += str(index % 3)
            index //= 3
        parity %= 3
        parity = C.Cparity[parity]

        return int(ori[::-1] + str(parity % 3))

    @staticmethod
    def get_orientation_numpy(index: int) -> int:
        """
        Get orientation of corners of given index, using numpy.
        
        :speed_test timeit("C.get_orientation_numpy(1494)", setup="from file import C"): 1.5905366
        :param index: index number to be converted.
        :return: orientation of given index.
        """

        from numpy import base_repr

        n = base_repr(index, base=3)
        parity = int(n) % 3

        return int(f"{n}{C.Cparity[parity]}")


# There are 2048 possible ways to orientate the edges on a Rubik's Cube (2^11).
# NOTE: The first 11 edges determine the orientation of the last, hence 2^11 (sum(orientations)%2 = 0).
# The orientation of all the edges can be encoded using the binary number system.
# Each edge has a rotation o, o ∈ {0, 1}.
# EXAMPLE: The edge orientation 10000111100(1) -> 1084.
# The inverse can be applied to obtain the orientation of all the edges given it's index number.

class E:
    """
    Abstract Edge class.
    """

    @staticmethod
    def get_index(orientation: int) -> int:
        """
        Get index number of edge orientation.
        
        :speed_test timeit("E.get_index(111111111111)", setup="from file import E"): 0.357996600000007
        :param orientation: orientation of edges.
        :return: index number of given orientation.
        """

        return int(str(orientation)[:-1], 2)

    @staticmethod
    def get_orientation(index: int) -> int:
        """
        Get orientation of edges of given index.
        
        :speed_test timeit("E.get_orientation(1878)", setup="from file import E"): 2.9557498000000066
        :param index: index number to be converted.
        :return: orientation of given index.
        """

        parity = 0
        ori = ""
        for _ in range(11):
            parity += (index % 2)
            ori += str(index % 2)
            index //= 2

        return int(ori[::-1] + str(parity % 2))

    @staticmethod
    def get_orientation_numpy(index: int) -> int:
        """
        Get orientation of edges of given index, using numpy.
        
        :speed_test timeit("E.get_orientation_numpy(1878)", setup="from file import E"): 2.1355667999999994
        :param index: index number to be converted.
        :return: orientation of given index.
        """

        from numpy import binary_repr

        n = binary_repr(index)

        parity = sum([int(char) for char in str(n)]) % 2
        return int(f"{n}{parity}")
