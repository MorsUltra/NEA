from aenum import Enum, NoAlias, IntEnum
import numpy
postiveR = numpy.arange(1, 4)
negativeR = numpy.arange(-1, -4, -1)

posx, posy = numpy.meshgrid(postiveR, postiveR)
negx, negy = numpy.meshgrid(negativeR, negativeR)

pos3 = numpy.full_like(negx, 3)
neg3 = numpy.full_like(negx, -3)

centersR = numpy.arange(-1, 2)
centerx, centery = numpy.meshgrid(centersR, centersR)

edgesP = numpy.arange(1, 4)
edgesN = numpy.arange(-1, -4, -1)

eposx, eposy = numpy.meshgrid(edgesP, edgesP)
enegx, enegy = numpy.meshgrid(edgesN, edgesN)

cccolours = ["gray", "red", "orange", "green", "blue", "yellow"]
class ccolours(IntEnum):
    U = 0
    R = 1
    L = 2
    F = 3
    B = 4
    D = 5


class col_coords(Enum):
    # TODO find a better way to do this shit without using some alias functions
    _settings_ = NoAlias
    """
    facelet values for whole cube, used to reference the posisition in cube defintion string to find particular facelet_index
    """
    U0 = negx, posy, pos3
    U1 = centerx, eposy, pos3
    U2 = posx, posy, pos3
    U3 = enegx, centery, pos3
    U4 = centerx, centery, numpy.full_like(centery, 3)
    U5 = eposx, centery, pos3
    U6 = negx, negy, pos3
    U7 = centerx, enegy, pos3
    U8 = posx, negy, pos3
    R0 = pos3, negx, posy
    R1 = pos3, centerx, eposy
    R2 = pos3, posx, posy
    R3 = pos3, negx, centery
    R4 = numpy.full_like(centery, 3), centerx, centery
    R5 = pos3, posx, centery
    R6 = pos3, negx, negy
    R7 = pos3, centerx, negy
    R8 = pos3, posx, negy
    L0 = neg3, negx, posy
    L1 = neg3, centerx, posy
    L2 = neg3, posx, posy
    L3 = neg3, posx, centery
    L4 = numpy.full_like(centery, -3), centery, centerx
    L5 = neg3, negx, centery
    L6 = neg3, negx, negy
    L7 = neg3, centerx, negy
    L8 = neg3, posx, negy
    F0 = negx, neg3, posy
    F1 = centerx, neg3, posy
    F2 = posx, neg3, posy
    F3 = negx, neg3, centery
    F4 = centery, numpy.full_like(centery, -3), centerx
    F5 = posx, neg3, centery
    F6 = negx, neg3, negy
    F7 = centerx, neg3, negy
    F8 = posx, neg3, negy
    B0 = posx, pos3, posy
    B1 = centerx, pos3, posy
    B2 = negx, pos3, posy
    B3 = posx, pos3, centery
    B4 = centerx, numpy.full_like(centery, 3), centery
    B5 = negx, pos3, centery
    B6 = posx, pos3, negy
    B7 = centerx, pos3, negy
    B8 = negx, pos3, negy
    D0 = negx, negy, neg3
    D1 = centerx, negy, neg3
    D2 = posx, negy, neg3
    D3 = negx, centery, neg3
    D4 = centery, centerx, numpy.full_like(centery, -3)
    D5 = posx, centery, neg3
    D6 = negx, posy, neg3
    D7 = centerx, posy, neg3
    D8 = posx, posy, neg3