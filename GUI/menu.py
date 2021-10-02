from random import randint
import pygame
import sys
from pygame.locals import *
import os
from GUI.pygame_facelets import load
from definitions.cubie_cube import cubiecube
from definitions.facelet_cube import facelet_cube
from definitions.cubedefs import urf_facelet_indices
from definitions.moves import * # TODO bug with this import here somehow, no idea :')

screen_width = 1920
screen_height = 1080
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption("main menu")
screen.fill((40, 43, 48))

clock = pygame.time.Clock()


class cube():
    colours = ["White",
               "Green",
               "Red",
               "Orange",
               "Yellow",
               "Blue"]

    # moves = {"U":Umove, "F":Fmove, "R":Rmove, "L":Lmove, "D":Dmove, "B":Bmove}

    sides = ["U", "F", "R", "L", "D", "B"]

    def __init__(self, static=False, scaling=1):
        self.cubiecube = cubiecube()
        self.string = self.cubiecube.to_facelet_cube(facelet_cube())
        self.urf = self.get_urf()

        self.scaling = scaling
        self.loop_cnt = 0
        self.x_constant = 1
        self.y_constant = 1
        self.size = 55

        if static:
            self.rect = pygame.Rect(static[0], static[1], self.size, self.size)
        else:
            self.rect = pygame.Rect(randint(1, screen_width - self.size - 1), randint(1, screen_height - self.size - 1),
                                    self.size, self.size)

        # self.rect = pygame.Rect(20, 20,
        #                         self.size, self.size)
        resources = os.getcwd() + r"/lib"

        self.top, self.left, self.right = load(resources)

    def get_urf(self):
        return self.set_colours("".join([self.string[c] for c in urf_facelet_indices]))

    def set_colours(self, raw):
        for i, face in enumerate(self.sides):
            raw = raw.replace(face, self.colours[i][0])
        return raw

    # def move(self, move):
    #     self.cubiecube.MOVE(self.moves[move])
    #     self.string = self.cubiecube.to_facelet_cube((facelet_cube()))
    #     self.urf = self.get_urf()

    def dynamic_draw(self, screen):
        corners = [(self.rect.x, self.rect.y), (self.rect.x + self.size, self.rect.y + self.size),
                   (self.rect.x + self.size, self.rect.y), (self.rect.x, self.rect.y + self.size)]

        for coord in corners:
            if coord[0] >= screen_width or coord[0] <= 0:
                if coord[1] >= screen_height or coord[1] <= 0:
                    self.x_constant *= -1
                    self.y_constant *= -1
                    self.scramble()
                    break

                self.x_constant *= -1
                break

            if coord[1] >= screen_height or coord[1] <= 0:
                if coord[0] >= screen_width or coord[0] <= 0:
                    self.x_constant *= -1
                    self.y_constant *= -1
                    self.scramble()
                    break

                self.y_constant *= -1
                break

        self.rect.move_ip(1 * self.x_constant, 1 * self.y_constant)

        self.draw(screen)

    def draw(self, screen):
        rectx = self.rect.x
        recty = self.rect.y

        for i, face in enumerate(self.urf):
            side = i // 9
            x = i % 3
            y = (i // 3) % 3
            if side == 0:
                image = self.top[face.lower()]
                image = self.scale(image)
                screen.blit(image, (rectx + 23 * self.scaling + x * 12 * self.scaling- y * 12* self.scaling, recty + -1* self.scaling + x * 6* self.scaling + y * 6* self.scaling))
            elif side == 1:
                image = self.right[face.lower()]
                image = self.scale(image)
                screen.blit(image, (rectx + 35* self.scaling + x * 12* self.scaling, recty + 29* self.scaling - x * 6* self.scaling + y * 15* self.scaling))
            elif side == 2:
                image = self.left[face.lower()]
                image = self.scale(image)
                screen.blit(image, (rectx + -1* self.scaling + x * 12 * self.scaling, recty + 17* self.scaling + x * 6 * self.scaling + y * 15 * self.scaling))

    def scale(self, image):
        x, y = image.get_size()
        image = pygame.transform.scale(image, (int(x*self.scaling), int(y*self.scaling)))
        return image

    # def scramble(self):
    #     self.cubiecube.shuffle()
    #     self.string = self.cubiecube.to_facelet_cube(facelet_cube())
    #     self.urf = self.get_urf()


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

        if function:
            self.activate = function
        else:
            self.activate = self.dummy

    def dummy(self, screen):
        return

    def draw(self):
        if self.rounded:
            pygame.draw.rect(self.screen, self.background_colour, self.rect,
                             border_radius=int(min(self.dimensions) / 4))
        else:
            pygame.draw.rect(self.screen, self.background_colour, self.rect)

        self.screen.blit(self.text_shadow,
                         (self.position[0] + self.padding + self.shadow, self.position[1] + self.padding + self.shadow))
        self.screen.blit(self.text, (self.position[0] + self.padding, self.position[1] + self.padding))

    def is_pressed(self, mx, my):
        if self.rect.collidepoint((mx, my)):  # if mouse is over button
            return True
        else:
            return False


def solve(screen):
    running = True
    escape = button(screen, (screen_width - 215, 20), "Escape", 30, shadow_colour=(200, 0, 0))  # keep escape seperate

    click = False

    objects = []

    while running:
        clock.tick(400)

        screen.fill((40, 43, 48))

        mx, my = pygame.mouse.get_pos()

        image.dynamic_draw(screen)
        if click:
            if escape.is_pressed(mx, my):
                running = False

            for obj in objects:
                if obj.is_pressed(mx, my):
                    obj.activate(screen)

        for obj in objects:
            obj.draw()

        escape.draw()

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


def scramble_cube():
    pass


def generate(screen):
    running = True
    pos = (screen_width-900, 50)

    cc = cube(static=pos, scaling=11)

    escape = button(screen, (screen_width - 215, 20), "Escape", 30, shadow_colour=(200, 0, 0))

    scramble_cube = button(screen, (screen_width - 540, screen_height - 100), "Scramble cube", 43,
                           shadow_colour=(0, 0, 255))

    objects = [scramble_cube]

    click = False

    while running:
        clock.tick(400)


        screen.fill((40, 43, 48))

        mx, my = pygame.mouse.get_pos()

        if click:
            if escape.is_pressed(mx, my):
                running = False

            for obj in objects:
                if obj.is_pressed(mx, my):
                    obj.activate(screen)

        cc.move("R")
        cc.draw(screen)

        escape.draw()

        for obj in objects:  # draw out the objects
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


def main_menu(screen):
    solve_cube = button(screen, (40, 40), "solve cube", shadow_colour=(255, 0, 0), function=solve)

    generate_cube = button(screen, (40, 150), "generate cube", shadow_colour=(0, 255, 0), function=generate)

    objects = [solve_cube, generate_cube]

    click = False

    while True:
        clock.tick(400)

        screen.fill((40, 43, 48))

        image.dynamic_draw(screen)

        mx, my = pygame.mouse.get_pos()

        if click:

            for obj in objects:
                if obj.is_pressed(mx, my):
                    obj.activate(screen)

        for obj in objects:  # draw out the objects
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
main_menu(screen)
