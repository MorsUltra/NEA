def P4edge_coordst(self, index: int):
    """
    Function to set the permutation of the UD-slice edge permutation based off of the coordinate between 0 --> 23
    (4! - 1).

    :param index: the coordinate of the UD-slice edge permutation.
    """

    # Create an empty list of UD-slice edges.
    edges = [8, 9, 10, 11]
    # Create empty factoradic
    factoradic = []

    # Increase the radix with each of the 3 steps.
    for mixed_radix in range(2, 5):
        # Add the remainder to the factoradic to record how many (mixed_radix!) are a part of the number.
        factoradic.append(index % mixed_radix)
        # Remove (mixed_radix!) as a factor from index.
        index //= mixed_radix

    for i in range(3, 0, -1):
        self.ep[8 + i] = edges.pop(factoradic[i-1])

    self.ep[8] = edges[0]
