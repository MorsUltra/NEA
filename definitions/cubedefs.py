from enum import IntEnum
from typing import Union, Any
# penis

class axes(IntEnum):
    U = 0
    R = 1
    L = 2
    F = 3
    B = 4
    D = 5


facelet_to_col = ["U", "R", "L", "F", "B", "D", "X"]


class facelet_indices(IntEnum):
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


class urf_facelet_indices(IntEnum):
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
    F0 = 27
    F1 = 28
    F2 = 29
    F3 = 30
    F4 = 31
    F5 = 32
    F6 = 33
    F7 = 34
    F8 = 35


class corner_indices(IntEnum):
    URF = 0
    UFL = 1
    ULB = 2
    UBR = 3

    DFR = 4
    DLF = 5
    DBL = 6
    DRB = 7


class edge_indices(IntEnum):
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
    BL = 10
    BR = 11


corner_facelet_indices: list[tuple[facelet_indices, facelet_indices, facelet_indices]] = [
    (facelet_indices.U8, facelet_indices.R0, facelet_indices.F2),
    (facelet_indices.U6, facelet_indices.F0, facelet_indices.L2),
    (facelet_indices.U0, facelet_indices.L0, facelet_indices.B2),
    (facelet_indices.U2, facelet_indices.B0, facelet_indices.R2),
    (facelet_indices.D2, facelet_indices.F8, facelet_indices.R6),
    (facelet_indices.D0, facelet_indices.L8, facelet_indices.F6),
    (facelet_indices.D6, facelet_indices.B8, facelet_indices.L6),
    (facelet_indices.D8, facelet_indices.R8, facelet_indices.B6)]

edge_facelet_indices: list[Union[tuple[facelet_indices, facelet_indices], Any]] = [

    (facelet_indices.U5, facelet_indices.R1),
    (facelet_indices.U7, facelet_indices.F1),
    (facelet_indices.U3, facelet_indices.L1),
    (facelet_indices.U1, facelet_indices.B1),

    (facelet_indices.D5, facelet_indices.R7),
    (facelet_indices.D1, facelet_indices.F7),
    (facelet_indices.D3, facelet_indices.L7),
    (facelet_indices.D7, facelet_indices.B7),

    (facelet_indices.F5, facelet_indices.R3),
    (facelet_indices.F3, facelet_indices.L5),
    (facelet_indices.B5, facelet_indices.L3),
    (facelet_indices.B3, facelet_indices.R5)]

corner_axes = [
    (axes.U, axes.R, axes.F),
    (axes.U, axes.F, axes.L),
    (axes.U, axes.L, axes.B),
    (axes.U, axes.B, axes.R),

    (axes.D, axes.F, axes.R),
    (axes.D, axes.L, axes.F),
    (axes.D, axes.B, axes.L),
    (axes.D, axes.R, axes.B)]

edge_axes = [
    (axes.U, axes.R),
    (axes.U, axes.F),
    (axes.U, axes.L),
    (axes.U, axes.B),

    (axes.D, axes.R),
    (axes.D, axes.F),
    (axes.D, axes.L),
    (axes.D, axes.B),

    (axes.F, axes.R),
    (axes.F, axes.L),
    (axes.B, axes.L),
    (axes.B, axes.R)]

raw_colours = ["White",
               "Green",
               "Red",
               "Orange",
               "Yellow",
               "Blue"]
