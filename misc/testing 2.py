from definitions.cubie_cube import CubieCube as C
from definitions.cubedefs import *

cpU = [Corner_Indices.UBR, Corner_Indices.URF, Corner_Indices.UFL, Corner_Indices.ULB, Corner_Indices.DFR,
       Corner_Indices.DLF, Corner_Indices.DBL, Corner_Indices.DRB]
coU = [0, 0, 0, 0, 0, 0, 0, 0]
epU = [Edge_Indices.UB, Edge_Indices.UR, Edge_Indices.UF, Edge_Indices.UL, Edge_Indices.DR, Edge_Indices.DF,
       Edge_Indices.DL, Edge_Indices.DB, Edge_Indices.FR, Edge_Indices.FL, Edge_Indices.BL, Edge_Indices.BR]
eoU = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

c = C(data=[cpU, coU, epU, eoU])
