import math
import os
import random
import sys
import threading
from itertools import count

import pygame
from pygame.locals import *

from GUI.pygame_facelets import load_facelets as load
from definitions.cubedefs import URF_Facelet_Indices
from definitions.cubie_cube import CubieCube
from definitions.facelet_cube import Facelet_Cube
from initialising.solve import Solver

screen_width = 1920
screen_height = 1080
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption("main menu")
screen.fill((40, 43, 48))

clock = pygame.time.Clock()


class BooleanTracker:
    def __init__(self, p=False):
        self.b = p

    def toggle(self):
        if self.b:
            self.b = False
        else:
            self.b = True

    def get_status_string(self):
        if self.b:
            return "True"
        else:
            return "False"

    def get_status_raw(self):
        return self.b

    def set(self, t):
        self.b = t


class Solution:
    move_antithesis = {1: 3,
                       3: 1,
                       2: 2}
    """
    Just going to need to track a few variables:
        need to be able to draw the cube
        need to be able to display empty cubes
        need to track current position and adjust it
        need to be able to pull solution from other objects
        need to handle two solutions for scrolling and other functions
    """

    def __init__(self, c):
        self.p = 0
        self.q = math.inf

        self.moves, self.powers = None, None
        self.formatted_solution = None

        self.current_step = Text(screen, None, (442, 958), background_colour=(0, 0, 0), text_colour=(220, 170, 170),
                                 tracking=True, track_target=self.get_current_move, size=70,
                                 word_limit=1)

        self.scrolling_solution = Text(screen, None, (600, 980), background_colour=(0, 0, 0), tracking=True,
                                       track_target=self.get_scrolling_moves, size=47)

        self.cubiecube = c.cubiecube

        self.raw_solution_tracking_target = c.get_raw_solutions
        self.formatted_solution_tracking_target = c.get_formatted_solutions

        self.cube_arr = [Cube(static=(300, 160), scaling=7, show_all=True, cc=self.cubiecube, solve=True),
                         Cube(cc=self.cubiecube, static=(900, 300), scaling=5),
                         Cube(cc=self.cubiecube, static=(1300, 360), scaling=4),
                         Cube(cc=self.cubiecube, static=(1625, 420), scaling=3)]

        self.__empty = True
        self.update()

    def get_current_move(self):
        if self.formatted_solution and self.p <= self.q:
            return self.formatted_solution[self.p]
        else:
            return None

    def get_scrolling_moves(self):
        if self.formatted_solution and self.p < self.q:
            return " ".join(self.formatted_solution[self.p + 1:])
        else:
            if self.formatted_solution:
                return "..."
            else:
                return None

    def update(self):
        if not self.__empty:
            return

        update = self.raw_solution_tracking_target()
        if update:
            self.__empty = False
            self.formatted_solution = self.formatted_solution_tracking_target()
            self.formatted_solution = self.formatted_solution.split()
            self.moves, self.powers = update
            self.q = len(self.moves) - 1
            self.set_cube_positions()
        else:
            return

    def set_cube_positions(self):  # just for setting
        for i, c in enumerate(self.cube_arr):
            if self.p + i > self.q:
                continue
            moves = self.moves[self.p:self.p + i]
            powers = self.powers[self.p:self.p + i]

            c.move(moves, powers)

    def next(self):
        if self.__empty:
            return

        if self.p <= self.q:
            for i, c in enumerate(self.cube_arr):
                if self.p + i > self.q:
                    continue
                move = [self.moves[self.p + i]]
                power = [self.powers[self.p + i]]
                c.move(move, power)
            if self.p <= self.q:
                self.p += 1
        else:
            return

    def previous(self):
        if self.__empty:
            return

        if self.p == 0:
            return

        self.p -= 1
        t = len(self.cube_arr)

        for i, c in enumerate(self.cube_arr):
            if self.p + i > self.q:
                continue
            move = [self.moves[self.p + i]]
            power = self.powers[self.p + i]
            power = [self.move_antithesis[power]]
            c.move(move, power)

    def reset(self, c):
        self.cubiecube = c.cubiecube

        self.raw_solution_tracking_target = c.get_raw_solutions
        self.formatted_solution_tracking_target = c.get_formatted_solutions

        self.cube_arr = [Cube(static=(300, 160), scaling=7, show_all=True, cc=self.cubiecube, solve=True),
                         Cube(cc=self.cubiecube, static=(900, 300), scaling=5),
                         Cube(cc=self.cubiecube, static=(1300, 360), scaling=4),
                         Cube(cc=self.cubiecube, static=(1625, 420), scaling=3)]

        self.__empty = True
        self.update()

    def draw(self):
        self.update()
        for cube in self.cube_arr:
            cube.draw()

        self.current_step.draw()
        self.scrolling_solution.draw()


class Counter:
    def __init__(self, starting, upper_limit=float("inf"), lower_limit=0):
        self._counter = starting
        self._q = lower_limit
        self._p = upper_limit

    def _check_bounds(self):
        if self._counter < self._q:
            self._counter = self._q
        elif self._counter > self._p:
            self._counter = self._p

    def __iadd__(self, other):
        self._counter += other
        self._check_bounds()

    def increment(self):
        self._counter += 1
        self._check_bounds()

    def decrement(self):
        self._counter -= 1
        self._check_bounds()

    def get_size(self):
        return str(self._counter)


class Cube:
    colours = ["White",
               "Green",
               "Red",
               "Orange",
               "Yellow",
               "Blue"]  # TODO just do some mapping here to map sides to a colour - honestly stupid

    sides = ["U", "R", "L", "F", "B", "D"]

    converter = dict(zip(sides, range(0, 6)))

    def __init__(self, static=False, scaling=1, cc=None,
                 show_all=False, solve=False):

        self.cubiecube = CubieCube(data=cc.to_data_arr()) if cc else CubieCube()
        self.string = self.cubiecube.to_facelet_string(Facelet_Cube())
        self.convert_string_int()
        self.scaling = scaling
        self.x_constant = -1
        self.y_constant = -1
        self.x = 72 * scaling
        self.y = 81 * scaling
        self.moves = []
        self.power = []
        self._mode = show_all
        self.solution = None
        self.__thread_started = False

        if static:
            self.rect = pygame.Rect(*static, self.x, self.y)
        else:
            self.rect = pygame.Rect(200, 200, self.x, self.y)
            # self.rect = pygame.Rect(random.randint(1, screen_width - self.x - 1),
            #                         random.randint(1, screen_height - self.y - 1),
            #                         self.x, self.y)

        resources = os.getcwd() + r"\lib\facelets"

        self.facelets = load(resources)

        if solve:
            self.solve_thread = threading.Thread(target=self.find_solutions, daemon=True)

    def clean(self, cc=None):
        self.cubiecube = cc if cc else CubieCube()
        self.string = self.cubiecube.to_facelet_string(Facelet_Cube())
        self.convert_string_int()
        self.moves = []
        self.power = []

    def find_solutions(self):
        s = Solver(self.cubiecube)
        print("solving")
        self.solution = s.find_solutions()
        print("found solution")

    def solve(self):
        if not self.__thread_started:
            self.__thread_started = True
            self.solve_thread.start()
        else:
            return

    def get_raw_solutions(self):
        if self.solution is not None:
            return self.solution
        else:
            return None

    def get_formatted_solutions(self):
        if self.solution is not None:
            return self.format_movespower(*self.solution)
        else:
            return None

    def change_scaling(self, scaling):
        self.scaling = scaling
        self.x = 72 * scaling
        self.y = 81 * scaling

    def move_cube(self, static):
        self.rect = pygame.Rect(static[0], static[1], self.x, self.y)

    def toggle_mode(self):
        self._mode = False if self._mode else True

    def get_urf(self, string):
        return self.set_colours("".join([string[c] for c in URF_Facelet_Indices]))

    def set_colours(self, raw):
        for i, face in enumerate(self.sides):
            raw = raw.replace(face, self.colours[i][0])
        return raw

    def convert_string_int(self):
        self.string = [self.converter[l] for l in self.string]

    def get_text_scramble(self):
        if len(self.moves) == 0:
            return "None"
        raw = " ".join(["".join(map(str, tup)) for tup in zip([self.sides[move] for move in self.moves], self.power)])
        raw = raw.replace("3", "'")
        raw = raw.replace("1", "")
        return raw

    def format_movespower(self, moves, power):
        if len(moves) == 0:
            return "None"
        raw = " ".join(["".join(map(str, tup)) for tup in zip([self.sides[move] for move in moves], power)])
        raw = raw.replace("3", "'")
        raw = raw.replace("1", "")
        return raw

    def move(self, moves, power):
        self.moves += moves
        self.power += power
        self.cubiecube.MOVE_arr(moves, power)

        self.string = self.cubiecube.to_facelet_string((Facelet_Cube()))
        self.convert_string_int()

    def shuffle(self):
        self.cubiecube.shuffle()
        self.string = self.cubiecube.to_facelet_string(Facelet_Cube())
        self.convert_string_int()

    def dynamic_draw(self):
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

        self.draw()

    def draw(self):
        rectx = self.rect.x + 23 * self.scaling
        recty = self.rect.y - 1 * self.scaling

        for i, colour in enumerate(self.string):
            image = self.facelets[i // 9][colour]
            image = self.scale(image)
            relative_side = i % 9
            x = relative_side % 3
            y = relative_side // 3
            match i // 9:
                case 0:
                    screen.blit(image, (rectx + x * 12 * self.scaling - y * 12 * self.scaling,
                                        recty + x * 6 * self.scaling + y * 6 * self.scaling))
                case 1:
                    screen.blit(image, (12 * self.scaling + rectx + x * 12 * self.scaling,
                                        30 * self.scaling + recty - x * 6 * self.scaling + y * 15 * self.scaling))
                case 2 if self._mode:
                    screen.blit(image, (-60 * self.scaling + rectx + x * 12 * self.scaling,
                                        recty + x * 6 * self.scaling + y * 15 * self.scaling))
                case 3:
                    screen.blit(image, (-24 * self.scaling + rectx + x * 12 * self.scaling,
                                        18 * self.scaling + recty + x * 6 * self.scaling + y * 15 * self.scaling))
                case 4 if self._mode:
                    screen.blit(image, (36 * self.scaling + rectx - 12 * self.scaling * x + 12 * self.scaling * y,
                                        6 * self.scaling + recty - 6 * self.scaling * x - 6 * self.scaling * y))
                case 5 if self._mode:
                    screen.blit(image, (-36 * self.scaling + rectx + x * 12 * self.scaling - y * 12 * self.scaling,
                                        63 * self.scaling + recty + x * 6 * self.scaling + y * 6 * self.scaling))

    def scale(self, image):
        x, y = image.get_size()
        image = pygame.transform.scale(image, (int(x * self.scaling), int(y * self.scaling)))
        return image


class Text:
    font_path = os.getcwd() + r"\lib\BACKTO1982.TTF"

    def __init__(self, screen, text, position, size=40, rounded=True, background_colour=(0, 0, 0),
                 text_colour=(255, 255, 255), padding=10, max_width=None, background=True, tracking=False,
                 track_target=None, word_limit=None):

        self.font = pygame.font.Font(self.font_path, size)

        self.size = size

        self.screen = screen

        self.rounded = rounded

        self.background = background

        self.max_width = max_width

        self.position = position

        self.background_colour = background_colour

        self.text_colour = text_colour

        self.text = text

        self.padding = padding if background else 0

        self.word_limit = word_limit

        if tracking:
            self.tracking = True
            self.get_variable_state = track_target
        else:
            self.tracking = False

        if self.text is not None:
            if max_width:
                self.lines = [self.font.render(line.strip(), False, self.text_colour) for line in
                              self.line_cropper(self.text, self.max_width)]
            else:
                self.lines = [self.font.render(self.text, False, self.text_colour)] if self.text else []

            if word_limit:
                self.text = self.text[:self.word_cropper(self.text, word_count=self.word_limit)]

    def word_cropper(self, string, seperator=" ", word_count=1):
        count = 0
        for i, char in enumerate(string):
            if char == seperator:
                count += 1
                if count == word_count:
                    return i
        return

    def get_y(self):
        ys = max([line.get_height() for line in self.lines])
        return ys

    def get_x(self):
        xs = max([line.get_width() for line in self.lines])
        return xs

    def line_cropper(self, t: str, max_width: int) -> list:
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

        return lines

    def set_text(self, text):
        self.text = text
        if self.word_limit:
            self.text = self.text[:self.word_cropper(self.text,
                                                     self.word_limit)]  # TODO can probably put all of this in a function - it's occuring too much
        self.lines = self.line_cropper(self.text, self.max_width)

    def _update_text(self):
        update = self.get_variable_state()
        if update is None:
            return -1
        else:
            self.text = self.get_variable_state()
            if self.word_limit:
                self.text = self.text[:self.word_cropper(self.text, word_count=self.word_limit)]
            if self.max_width:
                self.lines = self.line_cropper(self.text, self.max_width)
            return 1

    def draw(self):
        if self.tracking:
            match self._update_text():
                case 1:  # If text has been updated
                    if self.max_width:
                        self.lines = [self.font.render(line.strip(), False, self.text_colour) for line in
                                      self.line_cropper(self.text, self.max_width)]
                    else:
                        self.lines = [self.font.render(self.text, False, self.text_colour)] if self.text else []
                case -1:  # If text has not been updated
                    pass

        if self.text is None:
            return
        else:
            for y, line in enumerate(self.lines):
                if self.background:
                    pygame.draw.rect(self.screen, self.background_colour,
                                     pygame.Rect(self.position[0],
                                                 self.position[1] + self.size * y + 2 * self.padding * y,
                                                 line.get_width() + self.padding * 2,
                                                 line.get_height() + self.padding * 2),
                                     border_radius=int(min(line.get_size()) / 4))

                self.screen.blit(line,
                                 (self.position[0] + self.padding,
                                  self.position[1] + self.size * y + self.padding * (2 * y + 1)))


class Button:
    shadow_offset = 5
    padding = 10

    def __init__(self, screen, position, functions=None):
        if functions:
            self.__functions__ = functions
        else:
            self.__functions__ = []

        self.screen = screen

        self.position = position

    def run(self):
        for function in self.__functions__:
            function()

    # --------------- Abstract methods ------------------ #

    def is_pressed(self):
        """Abstract method for subclass override"""
        pass

    def draw(self):
        """Abstract method for subclass override"""
        pass


class ImageButton(Button):
    def __init__(self, screen, position, image_path, scaling=0, rotation=0, functions=None):
        super().__init__(screen, position, functions)

        self.scaling = scaling if scaling else 1

        self.image = pygame.image.load(image_path).convert()
        self.image.set_colorkey((0, 0, 0))

        if scaling:
            self.scale_image(scaling)

        if rotation:
            self.rotate_image(rotation)

    def rotate_image(self, rotation):
        self.image = pygame.transform.rotate(self.image, rotation)

    def scale_image(self, scaling):
        x, y = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(x * self.scaling), int(y * self.scaling)))

    def draw(self):
        self.screen.blit(self.image, self.position)

    def is_pressed(self, mx, my):
        rect = self.image.get_rect()
        rect.x, rect.y = self.position[0], self.position[1]
        if rect.collidepoint(mx, my):
            return True
        return False


class TextButton(Button):
    shadow_offset = 5
    padding = 10

    font_path = os.getcwd() + r"\lib\BACKTO1982.TTF"

    def __init__(self, screen, position, text, size=40, padding=None, rounded=True, shadow_colour=(0, 0, 0),
                 text_colour=(255, 255, 255), background_colour=(0, 0, 0), functions=None):
        super().__init__(screen, position, functions)

        if padding:
            self.padding = padding

        self.size = size
        self.font = pygame.font.Font(self.font_path, size)

        self.text_colour = text_colour

        self.text = self.font.render(text, False, self.text_colour)

        self.size = size if size else 40

        self.rounded = rounded

        self.shadow_colour = shadow_colour

        self.background_colour = background_colour

        self.text_shadow = self.font.render(text, False, self.shadow_colour)

        self.dimensions = self.text.get_width() + 2 * (
                self.padding + self.shadow_offset), self.text.get_height() + 2 * (self.padding + self.shadow_offset)

        self.rect = pygame.Rect(*self.position, *self.dimensions)

    def draw(self):
        if self.rounded:
            pygame.draw.rect(self.screen, self.background_colour, self.rect,
                             border_radius=int(min(self.dimensions) / 4))
        else:
            pygame.draw.rect(self.screen, self.background_colour, self.rect)

        self.screen.blit(self.text_shadow,
                         (self.position[0] + self.padding + self.shadow_offset,
                          self.position[1] + self.padding + self.shadow_offset))
        self.screen.blit(self.text, (self.position[0] + self.padding, self.position[1] + self.padding))

        self.rect = pygame.Rect(self.position[0], self.position[1], self.dimensions[0], self.dimensions[1])

    def is_pressed(self, mx, my):
        if self.rect.collidepoint((mx, my)):
            return True
        else:
            return False


class Square:
    size = 100
    id_iter = count()

    colour_map = {0: (255, 255, 255),
                  1: (255, 0, 0),
                  2: (255, 140, 0),
                  3: (0, 255, 0),
                  4: (0, 0, 255),
                  5: (255, 255, 0)}

    instances = []

    def __init__(self, anchor, initial_value=None, outline=None):

        self.anchor_x, self.anchor_y = anchor

        if outline:
            self.outline = outline
        else:
            self.outline = None

        self.rect = pygame.Rect(self.anchor_x, self.anchor_y, self.size,
                                self.size)

        if initial_value is not None:
            self.i = initial_value
            self.colour = self.colour_map[self.i]
        else:
            self.i = None
            self.colour = None

        self.id = next(self.id_iter)
        self.instances.append(self)

    @staticmethod
    def reset_counter():
        Square.id_iter = count()

    def is_pressed(self, mx, my):
        if self.rect.collidepoint(mx, my):
            return True
        else:
            return False

    def draw(self):
        if self.colour:
            pygame.draw.rect(screen, self.colour, self.rect)
        if self.outline:
            pygame.draw.rect(screen, self.outline, self.rect, width=2)

    def update_value(self, update):
        if update is not None:
            self.i = update
            self.colour = self.colour_map[self.i]

    def get_value(self):
        return self.i

    @staticmethod
    def collect_values():
        ids = list(range(54))
        l = [None] * 54
        for square in Square.instances:
            if square.id in ids:
                l[square.id] = square.get_value()

        return l

    def run(self):
        pass


class ColourSetter(Square):

    def __init__(self, anchor, initial_value, set_target, outline=(0, 0, 0)):
        super().__init__(anchor, initial_value=initial_value, outline=outline)
        self.set_target = set_target

    def run(self):
        self.set_target(self.i)


class ColourShower(Square):
    size = 200

    def __init__(self, anchor, set_target, initial_value=None, outline=(0, 0, 0)):
        super().__init__(anchor, initial_value=initial_value, outline=outline)
        self.get_i = set_target

    def draw(self):
        update = self.get_i()
        self.update_value(update)
        super().draw()


class ColourGetter(Square):
    size = 106

    def __init__(self, anchor, track_target, initial_value=None, outline=(0, 0, 0), locked=False):
        super().__init__(anchor, initial_value=initial_value, outline=outline)
        self.track_target = track_target
        self.locked = locked

    def run(self):
        if self.locked:
            return

        self.update_value(self.track_target())

    def toggle_lock(self):
        if self.locked:
            self.locked = False
        else:
            self.locked = True


class IntegerTracker:

    def __init__(self, j=None):
        self.i = j

    def set_i(self, j):
        self.i = j

    def get_i(self):
        return self.i


def input_cube_screen():
    Square.instances = []
    Square.reset_counter()

    axis_converter = {0: "U",
                      1: "R",
                      2: "L",
                      3: "F",
                      4: "B",
                      5: "D"}
    size = 116
    anchorx = 442
    anchory = 25
    t = IntegerTracker()

    U = [ColourGetter((anchorx + i % 3 * size, anchory + i // 3 * size), t.get_i) for i in range(9)]

    R = [ColourGetter((anchorx + 3 * size + i % 3 * size, anchory + 3 * size + i // 3 * size), t.get_i)
         for i in
         range(9)]

    L = [ColourGetter((anchorx - 3 * size + i % 3 * size, anchory + 3 * size + i // 3 * size), t.get_i)
         for i in
         range(9)]

    F = [ColourGetter((anchorx + i % 3 * size, anchory + 3 * size + i // 3 * size), t.get_i) for i in
         range(9)]

    B = [ColourGetter((anchorx + 6 * size + i % 3 * size, anchory + 3 * size + i // 3 * size), t.get_i)
         for i in
         range(9)]

    D = [ColourGetter((anchorx + i % 3 * size, anchory + 6 * size + i // 3 * size), t.get_i) for i in
         range(9)]

    b = BooleanTracker()

    valid_cube = Text(screen, "Valid Cube:", (980, 750), size=35)
    status = Text(screen, None, (1315, 753), track_target=b.get_status_string, tracking=True, size=30)

    current_colour_text = Text(screen, "Current colour", (25, 721), size=30, text_colour=(230, 230, 250))
    current_colour = ColourShower((25, 800), t.get_i)

    colour_setters = [ColourSetter((25 + i % 2 * 100, 25 + i // 2 * 100), i, set_target=t.set_i) for i in range(6)]

    faces = [U, R, L, F, B, D]

    for i, face in enumerate(faces):
        face[4].update_value(i)
        face[4].toggle_lock()

    collect_facelets = TextButton(screen, (980, 850), "Solve cube", size=60)

    running = True

    escape = TextButton(screen, (screen_width - 215, 20), "Escape", size=30, shadow_colour=(200, 0, 0))

    click = False

    drawable = [escape, *colour_setters, current_colour, *U, current_colour_text, *F, *R, *L, *B, *D, collect_facelets,
                status, valid_cube]

    objects = [*colour_setters, *U, *F, *R, *L, *B, *D]

    while running:
        clock.tick(400)

        screen.fill((40, 43, 48))

        fc_string = Square.collect_values()
        if None not in fc_string:
            fc = Facelet_Cube("".join([axis_converter[i] for i in
                                       fc_string]))  # TODO need to have facelet cube work with numbers instead of letters
            cc = fc.to_cubeie_cube(CubieCube())
            if fc.verify() == 1 and cc.verify() == 1:
                b.set(True)
            else:
                b.set(False)

        mx, my = pygame.mouse.get_pos()

        if click:
            if escape.is_pressed(mx, my):
                running = False

            if collect_facelets.is_pressed(mx, my):
                if b.b:
                    fc = Facelet_Cube("".join([axis_converter[i] for i in
                                               fc_string]))  # TODO need to have facelet cube work with numbers instead of letters
                    cc = fc.to_cubeie_cube(CubieCube())
                    return cc

            for obj in objects:
                if obj.is_pressed(mx, my):
                    obj.run()

        for obj in drawable:
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


def solve(cc=None):
    C = Cube(static=(300, 160), scaling=7, show_all=True, cc=cc, solve=True) if cc else Cube(static=(300, 160),
                                                                                             scaling=7,
                                                                                             show_all=True,
                                                                                             solve=True)

    running = True

    escape = TextButton(screen, (screen_width - 215, 20), "Escape", size=30, shadow_colour=(200, 0, 0))

    input_cube = TextButton(screen, (50, 980), "Input Cube", text_colour=(255, 255, 255), shadow_colour=(255, 0, 0))
    # currentstep = Text(screen, None, (442, 958), background_colour=(0, 0, 0), text_colour=(220, 170, 170),
    #                    tracking=True,
    #                    track_target=C.get_formatted_solutions, size=70, word_limit=1)
    #
    # sol = Text(screen, None, (600, 980), background_colour=(0, 0, 0), tracking=True,
    #            track_target=C.get_formatted_solutions, size=47)

    solve_cube = TextButton(screen, (50, 880), "Solve", size=50, text_colour=(255, 255, 255), shadow_colour=(255, 0, 0),
                            functions=[C.solve])
    click = False

    S = Solution(C)

    path = os.getcwd() + r"\lib"

    rarrow = ImageButton(screen, (750, 730), path + r"\arrows\rarrow.png", scaling=15,
                         rotation=180,
                         functions=[S.next])
    barrow = ImageButton(screen, (500, 730), path + r"\arrows\barrow.png", scaling=15,
                         functions=[S.previous])

    drawable = [escape, solve_cube, input_cube, S, rarrow, barrow]

    objects = [solve_cube, rarrow, barrow, input_cube]

    while running:
        clock.tick(400)

        screen.fill((40, 43, 48))

        mx, my = pygame.mouse.get_pos()

        if click:
            if escape.is_pressed(mx, my):
                running = False

            if input_cube.is_pressed(mx, my):
                m = input_cube_screen()
                if m == -1:
                    continue
                elif isinstance(m, CubieCube):
                    C.clean(m)
                    S.reset(C)

            for obj in objects:
                if obj.is_pressed(mx, my):
                    obj.run()

        for obj in drawable:
            obj.draw()

        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_LEFT:
                    barrow.run()
                elif event.key == K_RIGHT:
                    rarrow.run()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def scramble(cc, length):  # TODO not allowing sequential moves that are the same - B2 --> B2
    moves = [random.randint(0, 5) for x in range(length)]
    power = [random.randint(1, 3) for x in range(length)]
    cc.move(moves, power)


def generate():
    running = True
    POS = (screen_width - 900, 50)
    SCALING = 10

    cc = Cube(static=POS, scaling=SCALING)

    escape = TextButton(screen, (screen_width - 215, 20), "Escape", 30, shadow_colour=(200, 0, 0))

    scramble_cube = TextButton(screen, (screen_width - 540, screen_height - 100), "Scramble cube", 43,
                               shadow_colour=(0, 0, 255))

    solve_cube = TextButton(screen, (screen_width - 540, screen_height - 200), "Solve cube", 43,
                            shadow_colour=(0, 0, 255))

    title = Text(screen, "Scramble:", (50, 50), size=50,
                 text_colour=(0, 255, 255))

    s_pos = (50, title.position[1] + title.get_y() + title.padding * 2 + 20)
    s_size = 40
    s_bgcolour = (40, 43, 48)
    s_txtcolour = (0, 255, 255)

    cnt = Counter(24, lower_limit=1)

    s = Text(screen, "None", s_pos, size=s_size, background_colour=s_bgcolour, text_colour=s_txtcolour,
             max_width=900, tracking=True,
             track_target=cc.get_text_scramble)

    path = os.getcwd() + r"\lib"

    n = Text(screen, cnt.get_size(), (0, 876), background=False, size=80, tracking=True,
             track_target=cnt.get_size)

    barrow = ImageButton(screen, (50, 820), path + r"\arrows\barrow.png", scaling=15,
                         functions=[cnt.decrement])
    rarrow = ImageButton(screen, (500, 820), path + r"\arrows\rarrow.png", scaling=15,
                         rotation=180,
                         functions=[cnt.increment])

    n.position = (((barrow.position[0] + barrow.image.get_width()) + (rarrow.position[0])) / 2 - (n.get_x() / 2), 876)

    clickable = [barrow, rarrow]

    objects = [scramble_cube, solve_cube, title, escape, barrow, rarrow, s,
               n]

    click = False

    while running:
        clock.tick(400)

        screen.fill((40, 43, 48))

        mx, my = pygame.mouse.get_pos()

        if click:

            if escape.is_pressed(mx, my):
                running = False

            elif scramble_cube.is_pressed(mx, my):
                cc.clean()  # this is replacign cube, no more reference to old cube
                scramble(cc, int(cnt.get_size()))

            elif solve_cube.is_pressed(mx,
                                       my):  # these should be in button implementations somehow - how do you pass arguements with buttons?
                solve(cc.cubiecube)

            for obj in clickable:
                if obj.is_pressed(mx, my):
                    obj.run()

        cc.draw()
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


def main_menu():
    solve_cube = TextButton(screen, (40, 40), "solve cube", shadow_colour=(255, 0, 0))

    generate_cube = TextButton(screen, (40, 150), "generate cube", shadow_colour=(0, 255, 0), functions=[generate])

    clickable = [generate_cube]

    objects = [solve_cube, generate_cube]

    click = False

    while True:
        clock.tick(10000)

        screen.fill((40, 43, 48))

        image.dynamic_draw()

        mx, my = pygame.mouse.get_pos()

        if click:

            for obj in clickable:
                if obj.is_pressed(mx, my):
                    obj.run()

            if solve_cube.is_pressed(mx, my):
                solve()

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


# apparent hangups with smaller solves?
image = Cube(scaling=6)

main_menu()
