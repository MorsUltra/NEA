import pygame, sys
from pygame.locals import *
from .pygame_facelets import load
from definitions.cubedefs import urf_facelet_indices, raw_colours

resources = r"C:\Users\olive\Desktop\NEA\GUI\lib"

width = 100
mid = (width/2) - 12
pygame.init()
pygame.display.set_caption("Two-Phase Algorithm")
screen = pygame.display.set_mode((750, 750), 0, 32)
display = pygame.Surface((width, width))

top, left, right = load(resources)

def set_colours(raw: str, d = False):
    raw = raw.replace(" ", "")
    raw = "".join([raw[c] for c in urf_facelet_indices])

    cols = raw_colours[:]
    sides = ["U", "F", "R", "L", "D", "B"]
    if d:
        for i, face in enumerate(sides):
            raw = raw.replace(face, cols[i][0])
        return raw
    else:
        for face in sides:
            print(f"What colour is the {face} face?")
            for i, f in enumerate(cols):
                print(i, f)
            colour = int(input())
            raw = raw.replace(face, cols[colour][0])
            cols.pop(colour)
        return raw

def print_cube(urf):
    while True:
        display.fill((160, 160, 220))

        for i, face in enumerate(urf):
            side = i // 9
            if side == 0:
                x = i % 3
                y = (i // 3) % 3
                try:
                    display.blit(top[face.lower()], (mid + x * 12 - y * 12, 10 + x * 6 + y * 6))
                except:
                    continue
            elif side == 1:
                x = i % 3
                y = (i // 3) % 3
                try:
                    display.blit(right[face.lower()], (50 + x * 12, 40 - x * 6 + y * 15))
                except:
                    continue
            elif side == 2:
                x = i % 3
                y = (i // 3) % 3
                try:
                    display.blit(left[face.lower()], (14 + x * 12, 28 + x * 6 + y * 15))
                except:
                    continue
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()


def draw(from_import):
    urf = set_colours(from_import, d = True)

    print_cube(urf)

