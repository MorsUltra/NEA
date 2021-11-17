import os
import random
import sys

import pygame
from pygame.locals import *

from GUI.pygame_facelets import load
from definitions.cubedefs import urf_facelet_indices
from definitions.cubie_cube import cubiecube, MOVES as m
from definitions.facelet_cube import facelet_cube

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

    sides = ["U", "F", "R", "L", "D", "B"]

    moves = dict(zip(sides, m))

    def __init__(self, static=False, scaling=1):
        self.cubiecube = cubiecube()
        self.string = self.cubiecube.to_facelet_cube(facelet_cube())
        self.urf = self.get_urf(self.string)

        self.scaling = scaling
        self.loop_cnt = 0
        self.x_constant = 1
        self.y_constant = 1
        self.x = 72 * scaling
        self.y = 81 * scaling
        self.moves = []
        self.power = []

        if static:
            self.rect = pygame.Rect(static[0], static[1], self.x, self.y)
        else:
            self.rect = pygame.Rect(random.randint(1, screen_width - self.x - 1),
                                    random.randint(1, screen_height - self.y - 1),
                                    self.x, self.y)

        resources = os.getcwd() + r"/lib"

        self.top, self.left, self.right = load(resources)

    def get_urf(self, string):
        return self.set_colours("".join([string[c] for c in urf_facelet_indices]))

    def set_colours(self, raw):
        for i, face in enumerate(self.sides):
            raw = raw.replace(face, self.colours[i][0])
        return raw

    def get_scramble(self):
        return " ".join(["".join(map(str, tup)) for tup in zip([self.sides[move] for move in self.moves], self.power)])

    def move(self, moves, power):
        self.moves += moves
        self.power += power
        self.cubiecube.MOVE_arr(moves, power)
        self.string = self.cubiecube.to_facelet_cube((facelet_cube()))
        self.urf = self.get_urf(self.string)

    def shuffle(self):
        self.cubiecube.shuffle()
        self.string = self.cubiecube.to_facelet_cube(facelet_cube())
        self.urf = self.get_urf(self.string)

    def dynamic_draw(self, screen):
        corners = [self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright]

        for coord in corners:
            if coord[0] >= screen_width or coord[0] <= 0:
                if coord[1] >= screen_height or coord[1] <= 0:
                    self.x_constant *= -1
                    self.y_constant *= -1
                    self.shuffle()
                    break

                self.x_constant *= -1
                break

            if coord[1] >= screen_height or coord[1] <= 0:
                if coord[0] >= screen_width or coord[0] <= 0:
                    self.x_constant *= -1
                    self.y_constant *= -1
                    self.shuffle()
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
                # dimensions of image before scaling: 24 x 6
                screen.blit(image, (rectx + 23 * self.scaling + x * 12 * self.scaling - y * 12 * self.scaling,
                                    recty + -1 * self.scaling + x * 6 * self.scaling + y * 6 * self.scaling))
            elif side == 1:
                image = self.right[face.lower()]
                image = self.scale(image)
                screen.blit(image, (rectx + 35 * self.scaling + x * 12 * self.scaling,
                                    recty + 29 * self.scaling - x * 6 * self.scaling + y * 15 * self.scaling))
            elif side == 2:
                image = self.left[face.lower()]
                image = self.scale(image)
                screen.blit(image, (rectx + -1 * self.scaling + x * 12 * self.scaling,
                                    recty + 17 * self.scaling + x * 6 * self.scaling + y * 15 * self.scaling))

    def scale(self, image):
        x, y = image.get_size()
        image = pygame.transform.scale(image, (int(x * self.scaling), int(y * self.scaling)))
        return image

    # def scramble(self):
    #     self.cubiecube.shuffle()
    #     self.string = self.cubiecube.to_facelet_cube(facelet_cube())
    #     self.urf = self.get_urf()


class text:
    padding = 7

    font_path = os.getcwd() + r"\lib\BACKTO1982.TTF"

    def __init__(self, screen, t, position, size=40, rounded=True, background_colour=(0, 0, 0),
                 text_colour=(255, 255, 255), padding=0, max_width=None):

        self.font = pygame.font.Font(self.font_path, size)

        self.size = size

        self.screen = screen

        self.rounded = rounded

        if padding:
            self.padding = padding

        self.position = position

        self.background_colour = background_colour

        self.text_colour = text_colour

        self.text = t

        if max_width:
            self.lines = [self.font.render(line.strip(), False, self.text_colour) for line in
                          self.get_lines(self.text, max_width)]
        else:
            self.lines = [self.font.render(t, False, self.text_colour)]

    def get_y(self):
        ys = max([line.get_height() for line in self.lines])
        return ys

    def get_x(self):
        xs = max([line.get_width() for line in self.lines])
        return xs

    def get_lines(self, t, max_width):
        font = pygame.font.Font(self.font_path, self.size)
        lines = []

        while t:
            for i, letter in enumerate(t):
                f = font.render(t[:i], False, (255, 255, 255))
                size = f.get_width() + 2 * self.padding
                if size >= max_width:
                    lines.append(t[:i - 1])
                    t = t[i - 1:]
                    break

                if i + 1 == len(t):
                    lines.append(t)
                    return lines

    def draw(self):
        for y, line in enumerate(self.lines):
            pygame.draw.rect(self.screen, self.background_colour,
                             pygame.Rect(self.position[0], self.position[1] + self.size * y + 2 * self.padding * y,
                                         line.get_width() + self.padding * 2, line.get_height() + self.padding * 2),
                             border_radius=int(min(line.get_size()) / 4))
            self.screen.blit(line,
                             (self.position[0] + self.padding,
                              self.position[1] + self.size * y + self.padding * (2 * y + 1)))


class button:
    shadow_offset = 5
    padding = 10

    font_path = os.getcwd() + r"\lib\BACKTO1982.TTF"

    def __init__(self, screen, position, text, size=40, padding=None, rounded=True,
                 shadow_colour=(0, 0, 0),
                 text_colour=(255, 255, 255),
                 background_colour=(0, 0, 0),
                 function=None, image=False):

        self.font = pygame.font.Font(self.font_path, size)

        self.screen = screen

        self.rounded = rounded

        self.position = position

        if not image:
            if padding:
                self.padding = padding

            self.shadow_colour = shadow_colour
            self.text_colour = text_colour
            self.background_colour = background_colour

            self.text = text

            self.text = self.font.render(text, False, self.text_colour)
            self.text_shadow = self.font.render(text, False, self.shadow_colour)

            self.dimensions = self.text.get_width() + 2 * (
                    self.padding + self.shadow_offset), self.text.get_height() + 2 * (
                                      self.padding + self.shadow_offset)

            self.rect = pygame.Rect(self.position[0], self.position[1], self.dimensions[0], self.dimensions[1])

            self.draw = self.draw_no_image

        # This is a test of some hot shit
        # else:
        #     self.image_path = image
        #     self.image = pygame.image.load(self.image_path).convert()
        #     self.draw = self.draw_with_image

        if function:
            self.activate = function
        else:
            self.activate = self.dummy

    def dummy(self, screen):
        return

    def draw(self):
        pass

    def draw_no_image(self):
        if self.rounded:
            pygame.draw.rect(self.screen, self.background_colour, self.rect,
                             border_radius=int(min(self.dimensions) / 4))
        else:
            pygame.draw.rect(self.screen, self.background_colour, self.rect)

        self.screen.blit(self.text_shadow,
                         (self.position[0] + self.padding + self.shadow_offset,
                          self.position[1] + self.padding + self.shadow_offset))
        self.screen.blit(self.text, (self.position[0] + self.padding, self.position[1] + self.padding))

    def is_pressed(self, mx, my):
        if self.rect.collidepoint((mx, my)):  # if mouse is over button
            return True
        else:
            return False

class ImageButton(button):
    def __init__(self, screen, position, text, size=40, padding=None, rounded=True,
                 shadow_colour=(0, 0, 0),
                 text_colour=(255, 255, 255),
                 background_colour=(0, 0, 0),
                 function=None, image=False):

        self.font = pygame.font.Font(self.font_path, size)

        self.screen = screen

        self.rounded = rounded

        self.position = position

        if not image:
            if padding:
                self.padding = padding

            self.shadow_colour = shadow_colour
            self.text_colour = text_colour
            self.background_colour = background_colour

            self.text = text

            self.text = self.font.render(text, False, self.text_colour)
            self.text_shadow = self.font.render(text, False, self.shadow_colour)

            self.dimensions = self.text.get_width() + 2 * (
                    self.padding + self.shadow_offset), self.text.get_height() + 2 * (
                                      self.padding + self.shadow_offset)

            self.rect = pygame.Rect(self.position[0], self.position[1], self.dimensions[0], self.dimensions[1])

            self.draw = self.draw_no_image

        # This is a test of some hot shit
        # else:
        #     self.image_path = image
        #     self.image = pygame.image.load(self.image_path).convert()
        #     self.draw = self.draw_with_image

        if function:
            self.activate = function
        else:
            self.activate = self.dummy

    def draw_with_image(self):
        screen.blit(self.image, self.position)
        # TODO make a button subclass for images, buttons, escapes, etc.


class TextButton(button):
    def __init__(self, screen, position, text, size=40, padding=None, rounded=True,
                 shadow_colour=(0, 0, 0),
                 text_colour=(255, 255, 255),
                 background_colour=(0, 0, 0),
                 function=None, image=False):
        pass

    def draw_no_image(self):
        if self.rounded:
            pygame.draw.rect(self.screen, self.background_colour, self.rect,
                             border_radius=int(min(self.dimensions) / 4))
        else:
            pygame.draw.rect(self.screen, self.background_colour, self.rect)

        self.screen.blit(self.text_shadow,
                         (self.position[0] + self.padding + self.shadow_offset,
                          self.position[1] + self.padding + self.shadow_offset))
        self.screen.blit(self.text, (self.position[0] + self.padding, self.position[1] + self.padding))



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


def scramble(cc, length):
    moves = [random.randint(0, 5) for x in range(length)]
    power = [random.randint(1, 3) for x in range(length)]
    cc.move(moves, power)


def generate(screen):
    running = True
    POS = (screen_width - 900, 50)
    SCALING = 11

    s = None
    cc = cube(static=POS, scaling=SCALING)

    escape = button(screen, (screen_width - 215, 20), "Escape", 30, shadow_colour=(200, 0, 0))

    scramble_cube = button(screen, (screen_width - 540, screen_height - 100), "Scramble cube", 43,
                           shadow_colour=(0, 0, 255))

    title = text(screen, "Scramble:", (50, 50), size=50, background_colour=(60, 60, 60),
                 text_colour=(0, 0, 255))

    s_pos = (50, title.position[1] + title.get_y() + title.padding * 2 + 20)
    s_size = 40
    s_bgcolour = (60, 60, 60)
    s_txtcolour = (0, 255, 255)
    s = text(screen, "None", s_pos, size=s_size, background_colour=s_bgcolour, text_colour=s_txtcolour)

    clickable = []

    objects = [scramble_cube, title]

    click = False

    while running:
        clock.tick(400)

        screen.fill((40, 43, 48))

        mx, my = pygame.mouse.get_pos()

        if click:

            if escape.is_pressed(mx, my):
                running = False

            if scramble_cube.is_pressed(mx, my):
                cc = cube(static=POS, scaling=SCALING)
                scramble(cc, 30)

                s = text(screen, cc.get_scramble(), s_pos, size=s_size, background_colour=s_bgcolour,
                         text_colour=s_txtcolour, max_width=900)

            for obj in clickable:
                if obj.is_pressed(mx, my):
                    obj.activate(screen)

        escape.draw()
        cc.draw(screen)
        s.draw()

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

    clickable = [solve_cube, generate_cube]

    objects = [solve_cube, generate_cube]

    click = False

    while True:
        clock.tick(10000)

        screen.fill((40, 43, 48))

        image.dynamic_draw(screen)

        mx, my = pygame.mouse.get_pos()

        if click:

            for obj in clickable:
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


image = cube(scaling=6)

main_menu(screen)
