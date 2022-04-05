from definitions.cubedefs import *
from definitions.cubie_cube import CubieCube

# Create the U move.
cpU = [Corner_Indices.UBR, Corner_Indices.URF, Corner_Indices.UFL, Corner_Indices.ULB, Corner_Indices.DFR,
       Corner_Indices.DLF, Corner_Indices.DBL, Corner_Indices.DRB]
coU = [0, 0, 0, 0, 0, 0, 0, 0]
epU = [Edge_Indices.UB, Edge_Indices.UR, Edge_Indices.UF, Edge_Indices.UL, Edge_Indices.DR, Edge_Indices.DF,
       Edge_Indices.DL, Edge_Indices.DB, Edge_Indices.FR, Edge_Indices.FL, Edge_Indices.BL, Edge_Indices.BR]
eoU = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Create the R move.
cpR = [Corner_Indices.DFR, Corner_Indices.UFL, Corner_Indices.ULB, Corner_Indices.URF, Corner_Indices.DRB,
       Corner_Indices.DLF, Corner_Indices.DBL, Corner_Indices.UBR]
coR = [2, 0, 0, 1, 1, 0, 0, 2]
epR = [Edge_Indices.FR, Edge_Indices.UF, Edge_Indices.UL, Edge_Indices.UB, Edge_Indices.BR, Edge_Indices.DF,
       Edge_Indices.DL, Edge_Indices.DB, Edge_Indices.DR, Edge_Indices.FL, Edge_Indices.BL, Edge_Indices.UR]
eoR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Create the F move.
cpF = [Corner_Indices.UFL, Corner_Indices.DLF, Corner_Indices.ULB, Corner_Indices.UBR, Corner_Indices.URF,
       Corner_Indices.DFR, Corner_Indices.DBL, Corner_Indices.DRB]
coF = [1, 2, 0, 0, 2, 1, 0, 0]
epF = [Edge_Indices.UR, Edge_Indices.FL, Edge_Indices.UL, Edge_Indices.UB, Edge_Indices.DR, Edge_Indices.FR,
       Edge_Indices.DL, Edge_Indices.DB, Edge_Indices.UF, Edge_Indices.DF, Edge_Indices.BL, Edge_Indices.BR]
eoF = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

# Create the D move.
cpD = [Corner_Indices.URF, Corner_Indices.UFL, Corner_Indices.ULB, Corner_Indices.UBR, Corner_Indices.DLF,
       Corner_Indices.DBL, Corner_Indices.DRB, Corner_Indices.DFR]
coD = [0, 0, 0, 0, 0, 0, 0, 0]
epD = [Edge_Indices.UR, Edge_Indices.UF, Edge_Indices.UL, Edge_Indices.UB, Edge_Indices.DF, Edge_Indices.DL,
       Edge_Indices.DB, Edge_Indices.DR, Edge_Indices.FR, Edge_Indices.FL, Edge_Indices.BL, Edge_Indices.BR]
eoD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Create the L move.
cpL = [Corner_Indices.URF, Corner_Indices.ULB, Corner_Indices.DBL, Corner_Indices.UBR, Corner_Indices.DFR,
       Corner_Indices.UFL, Corner_Indices.DLF, Corner_Indices.DRB]
coL = [0, 1, 2, 0, 0, 2, 1, 0]
epL = [Edge_Indices.UR, Edge_Indices.UF, Edge_Indices.BL, Edge_Indices.UB, Edge_Indices.DR, Edge_Indices.DF,
       Edge_Indices.FL, Edge_Indices.DB, Edge_Indices.FR, Edge_Indices.UL, Edge_Indices.DL, Edge_Indices.BR]
eoL = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Create the B move.
cpB = [Corner_Indices.URF, Corner_Indices.UFL, Corner_Indices.UBR, Corner_Indices.DRB, Corner_Indices.DFR,
       Corner_Indices.DLF, Corner_Indices.ULB, Corner_Indices.DBL]
coB = [0, 0, 1, 2, 0, 0, 2, 1]
epB = [Edge_Indices.UR, Edge_Indices.UF, Edge_Indices.UL, Edge_Indices.BR, Edge_Indices.DR, Edge_Indices.DF,
       Edge_Indices.DL, Edge_Indices.BL, Edge_Indices.FR, Edge_Indices.FL, Edge_Indices.UB, Edge_Indices.DB]
eoB = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]


# Initialise the moves as cubes.
Umove = CubieCube(data=[cpU, coU, epU, eoU])
Rmove = CubieCube(data=[cpR, coR, epR, eoR])
Lmove = CubieCube(data=[cpL, coL, epL, eoL])
Fmove = CubieCube(data=[cpF, coF, epF, eoF])
Bmove = CubieCube(data=[cpB, coB, epB, eoB])
Dmove = CubieCube(data=[cpD, coD, epD, eoD])

MOVES = [Umove,
         Rmove,
         Lmove,
         Fmove,
         Bmove,
         Dmove]
