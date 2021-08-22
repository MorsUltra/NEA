from enum import IntEnum, Enum
from typing import List, Tuple, Union, Any




class colours(IntEnum):
    U = 0
    R = 1
    L = 2
    F = 3
    B = 4
    D = 5


class facelet_index(IntEnum):
    """
    facelet values for whole cube, used to reference the posisition in cube defintion string to find particular facelet_index
    """
    U0 = 0
    U1 = 1
    U2 = 2
    U3 = 3
    U4 = 4
    U5 = 5
    U6 = 6
    U7 = 7
    U8 = 8
    R0 = 9
    R1 = 10
    R2 = 11
    R3 = 12
    R4 = 13
    R5 = 14
    R6 = 15
    R7 = 16
    R8 = 17
    L0 = 18
    L1 = 19
    L2 = 20
    L3 = 21
    L4 = 22
    L5 = 23
    L6 = 24
    L7 = 25
    L8 = 26
    F0 = 27
    F1 = 28
    F2 = 29
    F3 = 30
    F4 = 31
    F5 = 32
    F6 = 33
    F7 = 34
    F8 = 35
    B0 = 36
    B1 = 37
    B2 = 38
    B3 = 39
    B4 = 40
    B5 = 41
    B6 = 42
    B7 = 43
    B8 = 44
    D0 = 45
    D1 = 46
    D2 = 47
    D3 = 48
    D4 = 49
    D5 = 50
    D6 = 51
    D7 = 52
    D8 = 53


class corner_index(IntEnum):
    URF = 0
    UFL = 1
    ULB = 2
    UBR = 3

    DFR = 4
    DLF = 5
    DBL = 6
    DRB = 7


class edge_index(IntEnum):
    UR = 0
    UF = 1
    UL = 2
    UB = 3

    DR = 4
    DF = 5
    DL = 6
    DB = 7

    FR = 8
    FL = 9
    BR = 10
    BL = 11


corner_facelet_index: list[tuple[facelet_index, facelet_index, facelet_index]] = [
    (facelet_index.U8, facelet_index.R0, facelet_index.F2),
    (facelet_index.U6, facelet_index.F0, facelet_index.L2),
    (facelet_index.U0, facelet_index.L0, facelet_index.B2),
    (facelet_index.U2, facelet_index.B0, facelet_index.R2),
    (facelet_index.D2, facelet_index.F8, facelet_index.R6),
    (facelet_index.D0, facelet_index.L8, facelet_index.F6),
    (facelet_index.D6, facelet_index.B8, facelet_index.L6),
    (facelet_index.D8, facelet_index.R8, facelet_index.B6)]

edge_facelet_index: list[Union[tuple[facelet_index, facelet_index], Any]] = [

    (facelet_index.U5, facelet_index.R1),
    (facelet_index.U7, facelet_index.F1),
    (facelet_index.U3, facelet_index.L1),
    (facelet_index.U1, facelet_index.B1),

    (facelet_index.D5, facelet_index.R7),
    (facelet_index.D1, facelet_index.F7),
    (facelet_index.D3, facelet_index.L7),
    (facelet_index.D7, facelet_index.B7),

    (facelet_index.F5, facelet_index.R3),
    (facelet_index.F3, facelet_index.L5),
    (facelet_index.B3, facelet_index.R5),
    (facelet_index.B5, facelet_index.L3)]

corner_colours = [
    (colours.U, colours.R, colours.F)
    , (colours.U, colours.F, colours.L)
    , (colours.U, colours.L, colours.B)
    , (colours.U, colours.B, colours.R)

    , (colours.D, colours.F, colours.R)
    , (colours.D, colours.L, colours.F)
    , (colours.D, colours.B, colours.L)
    , (colours.D, colours.R, colours.B)]

edge_colours = [
    (colours.U, colours.R)
    , (colours.U, colours.F)
    , (colours.U, colours.L)
    , (colours.U, colours.B)

    , (colours.D, colours.R)
    , (colours.D, colours.F)
    , (colours.D, colours.L)
    , (colours.D, colours.B)

    , (colours.F, colours.R)
    , (colours.F, colours.L)
    , (colours.B, colours.R)
    , (colours.B, colours.L)]
