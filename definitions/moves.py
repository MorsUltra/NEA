from definitions.cubedefs import corner_indices as c, edge_indices as e
from definitions.cubie_cube import cubiecube

cpU = [c.UBR, c.URF, c.UFL, c.ULB, c.DFR, c.DLF, c.DBL, c.DRB]
coU = [0, 0, 0, 0, 0, 0, 0, 0]
epU = [e.UB, e.UR, e.UF, e.UL, e.DR, e.DF, e.DL, e.DB, e.FR, e.FL, e.BL, e.BR]
eoU = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cpR = [c.DFR, c.UFL, c.ULB, c.URF, c.DRB, c.DLF, c.DBL, c.UBR]
coR = [2, 0, 0, 1, 1, 0, 0, 2]
epR = [e.FR, e.UF, e.UL, e.UB, e.BR, e.DF, e.DL, e.DB, e.DR, e.FL, e.BL, e.UR]
eoR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cpF = [c.UFL, c.DLF, c.ULB, c.UBR, c.URF, c.DFR, c.DBL, c.DRB]
coF = [1, 2, 0, 0, 2, 1, 0, 0]
epF = [e.UR, e.FL, e.UL, e.UB, e.DR, e.FR, e.DL, e.DB, e.UF, e.DF, e.BL, e.BR]
eoF = [0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0]

cpD = [c.URF, c.UFL, c.ULB, c.UBR, c.DLF, c.DBL, c.DRB, c.DFR]
coD = [0, 0, 0, 0, 0, 0, 0, 0]
epD = [e.UR, e.UF, e.UL, e.UB, e.DF, e.DL, e.DB, e.DR, e.FR, e.FL, e.BL, e.BR]
eoD = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cpL = [c.URF, c.ULB, c.DBL, c.UBR, c.DFR, c.UFL, c.DLF, c.DRB]
coL = [0, 1, 2, 0, 0, 2, 1, 0]
epL = [e.UR, e.UF, e.BL, e.UB, e.DR, e.DF, e.FL, e.DB, e.FR, e.UL, e.DL, e.BR]
eoL = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

cpB = [c.URF, c.UFL, c.UBR, c.DRB, c.DFR, c.DLF, c.ULB, c.DBL]
coB = [0, 0, 1, 2, 0, 0, 2, 1]
epB = [e.UR, e.UF, e.UL, e.BR, e.DR, e.DF, e.DL, e.BL, e.FR, e.FL, e.UB, e.DB]
eoB = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1]

Umove = cubiecube(cp=cpU, co=coU, ep=epU, eo=eoU)
Rmove = cubiecube(cp=cpR, co=coR, ep=epR, eo=eoR)
Lmove = cubiecube(cp=cpL, co=coL, ep=epL, eo=eoL)
Fmove = cubiecube(cp=cpF, co=coF, ep=epF, eo=eoF)
Bmove = cubiecube(cp=cpB, co=coB, ep=epB, eo=eoB)
Dmove = cubiecube(cp=cpD, co=coD, ep=epD, eo=eoD)
