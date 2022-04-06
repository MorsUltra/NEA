from functools import reduce
from math import comb as binomial_coefficient_calculator
from random import randint
from definitions.moves import *

from definitions.cubedefs import *


class CubieCube:
    """
    CubieCube class to handle cube based on it's cubies and coordinates.
    """

    MOVES = []
    # Set corner values to create parity.
    __Ocorner_parity_value = [0, 2, 1]

    def __init__(self, data: list[list, list, list, list] = None, moves: list = None):
        self.cp = data[0] if data else [0, 1, 2, 3, 4, 5, 6, 7]
        self.co = data[1] if data else [0, 0, 0, 0, 0, 0, 0, 0]
        self.ep = data[2] if data else [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.eo = data[3] if data else [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if moves:
            self.apply_move_array(*moves)

    @staticmethod
    def create_moves():
        """
        Class method to create the moves before the CubieCube class is handled.

        """

        CubieCube.MOVES = [CubieCube(data=[cpU, coU, epU, eoU]),
                           CubieCube(data=[cpR, coR, epR, eoR]),
                           CubieCube(data=[cpL, coL, epL, eoL]),
                           CubieCube(data=[cpF, coF, epF, eoF]),
                           CubieCube(data=[cpB, coB, epB, eoB]),
                           CubieCube(data=[cpD, coD, epD, eoD])]

    def is_solved(self) -> bool:
        """
        Function to check whether the cube is solved by default.

        :return: True if solved; False if not solved.
        """

        if self.to_data_array() == (
                [0, 1, 2, 3, 4, 5, 6, 7],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]):
            return True
        else:
            return False

    def verify(self) -> int:
        """
        Function to check whether cube is solvable via traditional means.

        :return: -1 if not solvable; 1 if solvable.
        """

        # If the edge parity is not equal the corner party the cube cannot be solved via traditional methods.
        if self.edge_parity != self.corner_parity:
            return -1
        else:
            return 1

    def to_data_array(self) -> tuple[list, list, list, list]:
        """
        Function to get the data of the cube in terms of its arrays of cubies.

        :return: Tuple of cube data - corner permutations, corner orientations, edge permutations, edge orientations.
        """

        return self.cp, self.co, self.ep, self.eo

    def to_facelet_string(self, facelet_cube) -> str:
        """
        Function to handle transition to FaceletCube object.

        :param facelet_cube: FaceletCube object to apply current cube data to.
        :return: Current cube in FaceletCube object form.
        """

        # Loop through the corners.
        for corner in Corner_Indices:
            # For each of the three facelets on the corner.
            for f in range(3):
                # Set the facelet in the string, with index as defined by the corner_facelet_indices,
                # as the respective facelet on the corner in iteration.
                facelet_cube.f[corner_facelet_indices[corner][(self.co[corner] + f) % 3]] = \
                    corner_axes[self.cp[corner]][f]

        # Loop through the edges.
        for edge in Edge_Indices:
            # For each of the two facelets on the edge.
            for e in range(2):
                # Set the facelet in the string, with index as defined by the edge_facelet_indices,
                # as the respective facelet on the corner in iteration.
                facelet_cube.f[edge_facelet_indices[edge][(self.eo[edge] + e) % 2]] = edge_axes[self.ep[edge]][e]

        # Change the string from Axis format to Colour format to allow for display.
        facelet_cube.f = [facelet_to_col[col] if col != -1 else facelet_to_col[i // 9] for i, col in
                          enumerate(facelet_cube.f)]

        return "".join(facelet_cube.f)

    def shuffle(self):
        """
        Method to shuffle cube object with no scramble string. I.e. random, valid coordinates have been picked for
        the cube.
        """

        # Pick random corner orientation and edge coordinates - the two are perfectly independent until permutation.
        self.o_corner_coords = randint(0, 2186)
        self.o_edge_coords = randint(0, 2047)

        # Find a combination of corner and edge permutations that is valid.
        while True:
            self.p_corner_coords = randint(0, 40319)
            self.p_edge_coords = randint(0, 479001599)
            if self.edge_parity != self.corner_parity:
                continue
            else:
                break

    def apply_move_array(self, moves: list, powers: list):
        """
        Method to apply a sequence of moves to the cube.

        :param moves: Moves to apply to the cube.
        :param powers: The power of the moves to apply to the cube.
        """

        for i, move in enumerate(moves):
            for power in range(powers[i]):
                self.apply_move(self.MOVES[move])

    def apply_move(self, to_apply: object):
        """
        Method to apply a move to the cube.

        :param to_apply: The move, in cube form, to be applied to the cube.
        """
        self.corner_move(to_apply)
        self.edge_move(to_apply)

    def corner_move(self, to_apply: object):
        """
        Method to apply move to the corners only.

        :param to_apply: The move to apply in cube form.
        """

        # Apply the move to corner permutation.
        self.corner_permutation_move(to_apply)
        # Apply the move to the corner orientation.
        self.corner_orientation_move(to_apply)

    def corner_orientation_move(self, to_apply: object):
        """
        Method to apply move to the corner orientation only.

        :param to_apply: The move to apply in cube form.
        """

        # Apply the move to the corner orientation.
        self.co = [(self.co[to_apply.cp[i]] + to_apply.co[i]) % 3 for i in range(8)]

    def corner_permutation_move(self, to_apply: object):
        """
        Method to apply move to the corner permutation only.

        :param to_apply: The move to apply in cube form.
        """

        # Apply the move to corner permutation.
        self.cp = [self.cp[to_apply.cp[i]] for i in range(8)]

    def edge_move(self, to_apply: object):
        """
        Method to apply move to the edges only.

        :param to_apply: The move to apply in cube form.
        """

        # Apply move to edge permutation.
        self.edge_permutation_move(to_apply)
        # Apply move to edge orientation.
        self.edge_orientation_move(to_apply)

    def edge_orientation_move(self, to_apply: object):
        """
        Method to apply move to edge orientation only.

        :param to_apply: The move to apply in cube form
        """

        # Apply move to edge orientation.
        self.eo = [(self.eo[to_apply.ep[i]] + to_apply.eo[i]) % 2 for i in range(12)]

    def edge_permutation_move(self, to_apply: object):
        """
        Method to apply move to edge permutation.

        :param to_apply: The move to apply in cube form.
        """

        # Apply the move to edge permutation.
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
    def o_corner_coords(self) -> int:
        """
        Getter function for corner orientation coordinate.
        
        :return: An integer number from 0 --> 2186 (3^7 - 1).
        """

        co = reduce(lambda variable_base, total: 3 * variable_base + total, self.co[:7])

        return co

    @o_corner_coords.setter
    def o_corner_coords(self, index: int):
        """
        Setter function for corner orientation coordinates. Takes an index and changes the cube's corner orientation
        to reflect that coordinate.

        @param index: index of corner orientation to change to.
        """

        self.co = [0] * 8
        # Loop through the 7 most significant bits, leaving the last to be implied.
        for i in range(6, -1, -1):
            # Collect the bit at index i which has significance 3^i; the remainder when divided by 3^i.
            self.co[i] = index % 3
            # Move to the next bit.
            index //= 3

        # Set the least significant bit by finding the bit required to make the sum a multiple of 3.
        self.co[7] = self.__Ocorner_parity_value[sum(self.co) % 3]

    @property
    def p_corner_coords(self) -> int:
        """
        Getter function for corner permutation coordinate.

        :return: A decimal number from 0 --> 40319 (8! - 1).
        """

        index = 0

        for p in range(7, 0, -1):
            more_significant_edges = 0
            for corner in self.cp[:p]:
                if corner > self.cp[p]:
                    more_significant_edges += 1

            index = (index + more_significant_edges) * p

        return index

    @p_corner_coords.setter
    def p_corner_coords(self, index: int):
        """
        Algorithm to set the permutation of corners of the coordinate between 0-40319.

        @param index: coordinate of corner permutation.
        """

        # Create an empty list of corners.
        corners = [7, 6, 5, 4, 3, 2, 1, 0]
        # Create empty factoradic number.
        factoradic = []

        # Increase the radix with each of the 7 steps.
        for mixed_radix in range(2, 8):
            # Add the remainder to the factoradic to record how many (mixed_radix!) are a part of the number.
            factoradic.append(index % mixed_radix)
            # Remove (mixed_radix!) as a factor from index.
            index //= mixed_radix

        # Add the final remainder to the factoradic.
        factoradic.append(index)

        # For each coefficient in the factoradic.
        for i in range(7, 0, -1):
            # Pop the relevant corner from the list per the factoradic number.
            self.cp[i] = corners.pop(factoradic[i - 1])

        # Append the final corner.
        self.cp[0] = corners[0]

    @property
    def o_edge_coords(self):  # working
        eo = reduce(lambda variable_base, total: 2 * variable_base + total, self.eo[:11])

        return eo

    @o_edge_coords.setter
    def o_edge_coords(self, index: int):
        """
        Algorithm to produce binary number of index range 2047 (2^11 - 1).

        @param index: Index of target edge orientation coordinate.
        """

        self.eo = [0] * 12
        for i in range(10, -1, -1):
            self.eo[i] = index % 2
            index //= 2

        self.eo[11] = sum(self.eo) % 2

    @property
    def p_edge_coords(self) -> int:
        """
        Getter function for the corner permutation coordinate.
        
        :return: A decimal number from 0 --> 479001599 (12! - 1).
        """

        index = 0

        for p in range(11, 0, -1):
            more_significant_edges = 0
            for edge in self.ep[:p]:
                if edge > self.ep[p]:
                    more_significant_edges += 1

            index = (index + more_significant_edges) * p

        return index

    @p_edge_coords.setter
    def p_edge_coords(self, index: int):
        """
        Function to set the permutation of the edges based off of the coordinate between 0-479001599 (12! - 1)

        :param index: the coordinate of the corner permutation.
        """

        # Create empty list of edges
        edges = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        # Create empty factoradic number.
        factoradic = []

        # Increase the radic with each of the 11 steps
        for mixed_radix in range(2, 12):
            # Add the remainder to the factoradic to record how many (mixed_radix!) are a part of the number.
            factoradic.append(index % mixed_radix)
            # Remove (mixed_radix!) as a factor from index.
            index //= mixed_radix

        # Add the final remainder to the factoradic.
        factoradic.append(index)

        # For each coefficient in the factoradic.
        for i in range(11, 0, -1):
            # Pop the relevant edge from the list per the factoradic number.
            self.ep[i] = edges.pop(factoradic[i - 1])

        # Append the final corner.
        self.ep[0] = edges[0]

    # ---------------------------------------------------------

    @property
    def p_8edge_coords(self) -> int:
        """
        Getter function for the 8-edge permutation coordinate.

        :return: A decimal from 0 --> 40319 (8! - 1).
        """

        index = 0

        for p in range(7, 0, -1):
            more_significant_edges = 0
            for edge in self.ep[:p]:
                if edge > self.ep[p]:
                    more_significant_edges += 1

            index = (index + more_significant_edges) * p

        return index

    @p_8edge_coords.setter
    def p_8edge_coords(self, index: int):
        """
        Function to set the permutation of the edges based off of the coordinate between 0 --> 40319 (8! - 1).

        :param index: the coordinate of the 8-edge permutation.
        """

        # Create empty list of 8-edges.
        edges = [7, 6, 5, 4, 3, 2, 1, 0]
        # Create empty factoradic number
        factoradic = []

        # Increase the radix with each of the 8 steps.
        for mixed_radix in range(2, 9):
            # Add the remainder to the factoradic to record how many (mixed_radix!) are a part of the number.
            factoradic.append(index % mixed_radix)
            # Remove (mixed_radix!) as a factor from index.
            index //= mixed_radix

        # Add the final remainder to the factoradic.
        factoradic.append(index)

        # For each coefficient in the factoradic.
        for i in range(7, 0, -1):
            # Pop the relevant edge from the list per the factoradic number.
            self.ep[i] = edges.pop(factoradic[i - 1])

        # Append the final corner.
        self.ep[0] = edges[0]

    @property
    def p_4edge_coords(self) -> int:
        """
        Getter function for the UD-slice edge permutation coordinate.

        :return: A decimal from 0 --> 23 (4! - 1)
        """

        # Separate the UD-slice edges.
        ep = self.ep[8:]

        index = 0

        for p in range(3, 0, -1):
            more_significant_edges = 0
            for edge in ep[:p]:
                if edge > ep[p]:
                    more_significant_edges += 1

            index = (index + more_significant_edges) * p

        return index

    @p_4edge_coords.setter
    def p_4edge_coords(self, index: int):
        """
        Function to set the permutation of the UD-slice edge permutation based off of the coordinate between 0 --> 23
        (4! - 1).

        :param index: the coordinate of the UD-slice edge permutation.
        """

        # Create an empty list of UD-slice edges.
        edges = [11, 10, 9, 8]
        # Create empty factoradic
        factoradic = []

        # Increase the radix with each of the 3 steps.
        for mixed_radix in range(2, 5):
            # Add the remainder to the factoradic to record how many (mixed_radix!) are a part of the number.
            factoradic.append(index % mixed_radix)
            # Remove (mixed_radix!) as a factor from index.
            index //= mixed_radix

        # For each coefficient in the factoradic.
        for i in range(3, 0, -1):
            # Pop the relevant UD-slice edges from the list per the factoradic number.
            self.ep[8 + i] = edges.pop(factoradic[i - 1])

        # Append the final corner.
        self.ep[8] = edges[0]

    @property
    def pos_udslice_coords(self) -> int:
        """
        Algorithm to get the UD-slice coordinate of the current edge permutation.

        :return: the UD-slice coordinate of the current cube.
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
                coordinate += binomial_coefficient_calculator(i, pieces_remaining - 1)

        return coordinate

    @pos_udslice_coords.setter
    def pos_udslice_coords(self, index: int):
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
                for j in range(i + 1):
                    self.ep[j] = other_edges
                    other_edges += 1
                break

            # Find the number of combinations of the remaining pieces that have a piece at position i.
            possible_combinations = binomial_coefficient_calculator(i, pieces_remaining - 1)

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
