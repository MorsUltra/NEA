import os
import pygame


def load(path):
    top = {}
    left = {}
    right = {}
    for f in os.listdir(path):
        if f.endswith(".png"):
            fpath = os.path.join(path, f)
            if f.startswith("t"):
                top[f[1:-4][0]] = pygame.image.load(fpath).convert()
            elif f.startswith("l"):
                left[f[1:-4][0]] = pygame.image.load(fpath).convert()
            elif f.startswith("r"):
                right[f[1:-4][0]] = pygame.image.load(fpath).convert()

    for c in [top, left, right]:
        for facelet in c:
            c[facelet].set_colorkey((0, 0, 0))

    return top, left, right
