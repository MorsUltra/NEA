# Permutations can use index numbers and algorithms to encode each state.
# The corner permutation is given by an index from 0-40319 (8! - 1).
# A natural order of corners is created. URF<UFL<ULB<UBR<DFR<DLF<DBL<DRB.
# EXAMPLE: the corner permutation DFR; UFL; ULB URF; DRB; DLF; DBL; UBR goes to:
# {_ 1 1 3 0 1 1 4} where each i has i corners higher in the hierarchy to it's left.
# {_ 1 1 3 0 1 1 4} goes to 21021, which is the decimal representation of b!4110311 (inverse of permutation).
# Variable base system is used (the factorial number system) to represent permutations.


class C:
    """
    Abstract corner class.

    :cvar corners: corners' "hierarchy".
    """

    corners: dict[str, int] = {
        "URF": 0,
        "UFL": 1,
        "ULB": 2,
        "UBR": 3,
        "DFR": 4,
        "DLF": 5,
        "DBL": 6,
        "DRB": 7,
    }

    @staticmethod
    def get_perm_divmod(perm_index: str) -> list:
        """
        Get permutations of corners of given index, using divmod.

        :speed_test timeit("get_perm_divmod(21021)", setup="from permutation_encoding import get_perm_divmod"): 2.002999
        :param perm_index: index number of target permutation.
        :return: returns inverse factoradic form of target permutation index.
        """

        factoradic = ""
        variable_base = 0
        while perm_index:
            variable_base += 1
            perm_index, remainder = divmod(perm_index, variable_base)
            factoradic += str(remainder)

        perm = [0] * 8
        corner_index = list(range(0, 8))
        for x in range(len(corner_index) - 1, -1, -1):
            perm[x] = corner_index.pop(x - int(factoradic[x]))

        return perm

    @staticmethod
    def get_perm(perm_index: str) -> list:
        """
        Get permutations of corners of given index.

        :speed_test timeit("get_perm(21021)", setup="from permutation_encoding import get_perm"): 1.8814547312100003
        :param perm_index: index number of target permutation.
        :return: returns inverse factoradic form of target permutation index.
        """

        factoradic = ""
        variable_base = 0
        while perm_index:
            variable_base += 1
            remainder = perm_index % variable_base
            perm_index //= variable_base
            factoradic += str(remainder)

        perm = [0] * 8
        corner_index = list(range(0, 8))
        for x in range(len(corner_index) - 1, -1, -1):
            perm[x] = corner_index.pop(x - int(factoradic[x]))

        return perm

    def get_index(self, permutation: list) -> int:
        """
        Get the index number of given permutation

        :speed_test ....: TODO time this function
        :param permutation: permutation of corners to convert. TODO tidy this up
        :return: returns index number of given permutation. TODO tidy this up
        """
        index = 0

        for p in range(7, 0, -1):
            higher = 0
            for corner in permutation[:p]:
                if self.corners[corner] > self.corners[permutation[p]]:
                    higher += 1

            index = (index + higher) * p

        return index


# The edge permutation is given by an index from 0-479001599 (12! - 1).
# A natural order of edges is created. UF<UL<UB<DR<DF<DL<DB<FR<FL<BL<BR


class E:
    """
    Abstract edge class.

    :cvar edges: edges' "hierarchy".
    """

    edges: dict[str, int] = {
        "UR": 0,
        "UF": 1,
        "UL": 2,
        "UB": 3,
        "DR": 4,
        "DF": 5,
        "DL": 6,
        "DB": 7,
        "FR": 8,
        "FL": 9,
        "BL": 10,
        "BR": 11
    }

    @staticmethod
    def get_perm_divmod(perm_index: str) -> int:
        """
        Get permutations of edges of given index, using divmod.

        :speed_test timeit("get_perm_divmod(21021)", setup="from permutation_encoding import get_perm_divmod"): 2.002999
        :param perm_index: index number of target permutation.
        :return: returns inverse factoradic form of target permutation index.
        """

        perm = ""
        variable_base = 0
        while perm_index:
            variable_base += 1
            perm_index, remainder = divmod(perm_index, variable_base)
            perm += str(remainder)

        return int(perm)

    @staticmethod
    def get_perm(perm_index: str) -> int:
        """
        Get permutations of corners of given index.

        :speed_test timeit("get_perm(21021)", setup="from permutation_encoding import get_perm"): 1.8814547312100003
        :param perm_index: index number of target permutation.
        :return: returns inverse factoradic form of target permutation index.
        """

        perm = ""
        variable_base = 0
        while perm_index:
            variable_base += 1
            remainder = perm_index % variable_base
            perm_index //= variable_base
            perm += str(remainder)

        return int(perm)
