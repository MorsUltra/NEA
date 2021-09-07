import pygame
import sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("main menu")
screen.fill((0, 0, 0))

font = pygame.font.SysFont(None, 20)
button_1 = pygame.Rect(50, 100, 200, 50)
button_2 = pygame.Rect(50, 200, 200, 50)

click = False


class button:
    def __init__(self, colour, position, dimensions):
        self.rect = pygame.Rect(position[0], position[1], dimensions[0], dimensions[1])
        self.colour = colour

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)

    def is_collide(self, mx, my):
        return self.rect.collidepoint((mx, my))


def testing():
    while True:
        print("testing")


def draw_text():
    pass


def main_loop():
    b1 = button((0, 0, 0), (50, 100), (200, 50))
    b2 = button((0, 0, 0), (50, 200), (200, 50))

    while True:

        screen.fill((255, 255, 255))

        mx, my = pygame.mouse.get_pos()

        if b1.is_collide(mx, my):
            if click:
                print("situation 1")

        if b2.is_collide(mx, my):
            if click:
                print("situation 2")

        b1.draw(screen)
        b2.draw(screen)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


main_loop()
