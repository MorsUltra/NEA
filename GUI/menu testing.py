from random import randint
import pygame
import sys
from pygame.locals import *
import os

screen_width = 900
screen_height = 900
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("main menu")
screen.fill((40, 43, 48))

clock = pygame.time.Clock()


class button:
    shadow = 5
    padding = 10

    font_path = os.getcwd() + r"\lib\BACKTO1982.TTF"

    def __init__(self, screen, position, text, size=40, padding=None, rounded=True,
                 shadow_colour=(0, 0, 0),
                 text_colour=(255, 255, 255),
                 background_colour=(0, 0, 0),
                 function=None):

        self.font = pygame.font.Font(self.font_path, size)

        self.screen = screen

        self.rounded = rounded

        if padding:
            self.padding = padding

        self.position = position

        self.shadow_colour = shadow_colour
        self.text_colour = text_colour
        self.background_colour = background_colour

        self.text = text
        self.fsize = 40

        self.text = self.font.render(text, False, self.text_colour)
        self.text_shadow = self.font.render(text, False, self.shadow_colour)

        self.dimensions = self.text.get_width() + 2 * (self.padding + self.shadow), self.text.get_height() + 2 * (
                self.padding + self.shadow)

        self.rect = pygame.Rect(self.position[0], self.position[1], self.dimensions[0], self.dimensions[1])

        self.function = function

    def draw(self):
        if self.rounded:
            pygame.draw.rect(self.screen, self.background_colour, self.rect,
                             border_radius=int(min(self.dimensions) / 4))
        else:
            pygame.draw.rect(self.screen, self.background_colour, self.rect)

        self.screen.blit(self.text_shadow,
                         (self.position[0] + self.padding + self.shadow, self.position[1] + self.padding + self.shadow))
        self.screen.blit(self.text, (self.position[0] + self.padding, self.position[1] + self.padding))

    def is_collide(self, mx, my):
        if self.rect.collidepoint((mx, my)):
            self.pressed()

    def pressed(self):
        if self.function:
            self.function(self.screen)
            return True
        else:
            return False


def solve(screen):
    running = True
    escape = button(screen, (screen_width - 215, 20), "Escape", 30, shadow_colour=(200, 0, 0))

    click = False

    objects = [escape]

    while running:

        screen.fill((40, 43, 48))

        mx, my = pygame.mouse.get_pos()

        if click:
            for obj in objects:
                running = obj.is_collide(mx, my)

        for obj in objects:
            obj.draw()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

class cube():
    def __init__(self):
        self.xconst = 1
        self.yconst = 1
        self.size = 55
        self.rect = pygame.Rect(randint(1, screen_width-self.size-1), randint(1, screen_height-self.size-1), self.size, self.size)

    def draw_cube(self, screen):

        dt = clock.tick(120)

        corners = [(self.rect.x, self.rect.y), (self.rect.x + self.size, self.rect.y + self.size), (self.rect.x+self.size, self.rect.y), (self.rect.x, self.rect.y+self.size)]

        for coord in corners:
            if coord[0] >= screen_width or coord[0] <= 0:
                if coord[1] >= screen_height or coord[1] <= 0:
                    self.xconst *= -1
                    self.yconst *= -1
                    self.scramble()
                    break

                self.xconst *= -1
                break
            if coord[1] >= screen_height or coord[1] <= 0:
                if coord[0] >= screen_width or coord[0] <= 0:
                    self.xconst *= -1
                    self.yconst *= -1
                    self.scramble()
                    break
                    # TODO some bug going down where it getting stuck in the corner somehow, maybe an offset check or something?

                self.yconst *= -1
                break

        self.rect.move_ip(0.2 * dt * self.xconst, 0.2 * dt * self.yconst)

        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def scramble(self):
        print("SCRAMBLE")




def main_loop(screen):

    b1 = button(screen, (40, 40), "solve cube", shadow_colour=(255, 0, 0), function=solve)

    objects = [b1]

    click = False

    while True:

        screen.fill((40, 43, 48))

        image.draw_cube(screen)



        mx, my = pygame.mouse.get_pos()

        if click:
            for obj in objects:
                obj.is_collide(mx, my)

        for obj in objects:
            obj.draw()

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




image = cube()
main_loop(screen)






