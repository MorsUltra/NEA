import os

import pygame


def load_facelets(path):
    facelets = [[None] * 6 for _ in range(6)]
    for f in os.listdir(path):
        axes = int(f[0])
        colour = int(f[1])
        fpath = os.path.join(path, f)
        image = pygame.image.load(fpath)
        image.set_colorkey((0, 0, 0))
        facelets[axes][colour] = image

    facelets[2] = facelets[3]
    facelets[5] = facelets[0]
    facelets[4] = facelets[0]

    return facelets
