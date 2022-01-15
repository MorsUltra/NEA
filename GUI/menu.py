import os
import random
import sys
import threading

import pygame
from pygame.locals import *

from GUI.pygame_facelets import load_facelets as load
from definitions.cubedefs import urf_facelet_indices
from definitions.cubie_cube import cubiecube, MOVES as m
from definitions.facelet_cube import facelet_cube
from initialising.solve import solver

screen_width = 1920
screen_height = 1080
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption("main menu")
screen.fill((40, 43, 48))

clock = pygame.time.Clock()


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
               "Blue"]

    sides = ["U", "R", "L", "F", "B", "D"]

    converter = dict(zip(sides, range(0, 6)))

    moves = dict(zip(sides, m))

    def __init__(self, static=False, scaling=1, cc=None,
                 show_all=False, solve=False):
        self.cubiecube = cc if cc else cubiecube()
        self.string = self.cubiecube.to_facelet_cube(facelet_cube())
        self.convert_string_int()
        self.scaling = scaling
        self.x_constant = 1
        self.y_constant = 1
        self.x = 72 * scaling
        self.y = 81 * scaling
        self.moves = []
        self.power = []
        self._mode = show_all
        self.solution = None

        if static:
            self.rect = pygame.Rect(*static, self.x, self.y)
        else:
            self.rect = pygame.Rect(random.randint(1, screen_width - self.x - 1),
                                    random.randint(1, screen_height - self.y - 1),
                                    self.x, self.y)

        resources = os.getcwd() + r"\lib\facelets"

        self.facelets = load(resources)

        if solve:
            self.solve_thread = threading.Thread(target=self.find_solutions)

    def find_solutions(self):
        s = solver(self.cubiecube, multithreading=False)
        print("solving")
        self.solution = s.find_solutions()
        print("found solution")

    def solve(self):
        self.solve_thread.start()

    def get_solutions(self):
        return self.solution

    def change_scaling(self, scaling):
        self.scaling = scaling
        self.x = 72 * scaling
        self.y = 81 * scaling

    def move_cube(self, static):
        self.rect = pygame.Rect(static[0], static[1], self.x, self.y)

    def toggle_mode(self):
        self._mode = False if self._mode else True

    def get_urf(self, string):
        return self.set_colours("".join([string[c] for c in urf_facelet_indices]))

    def set_colours(self, raw):
        for i, face in enumerate(self.sides):
            raw = raw.replace(face, self.colours[i][0])
        return raw

    def convert_string_int(self):
        self.string = [self.converter[l] for l in self.string]

    def get_scramble(self):
        raw = " ".join(["".join(map(str, tup)) for tup in zip([self.sides[move] for move in self.moves], self.power)])
        raw = raw.replace("3", "'")
        raw = raw.replace("1", "")
        return raw

    def move(self, moves, power):
        self.moves += moves
        self.power += power
        self.cubiecube.MOVE_arr(moves, power)
        self.string = self.cubiecube.to_facelet_cube((facelet_cube()))
        self.convert_string_int()

    def shuffle(self):
        self.cubiecube.shuffle()
        self.string = self.cubiecube.to_facelet_cube(facelet_cube())
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
                 track_target=None):

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

        if tracking:
            self.tracking = True
            self.variable = track_target
        else:
            self.tracking = False

        if max_width:
            self.lines = [self.font.render(line.strip(), False, self.text_colour) for line in
                          self.get_lines(self.text, max_width)]
        else:
            self.lines = [self.font.render(text, False, self.text_colour)]

    def update_text(self, text=None):
        if text is not None:
            self.text = text
        elif self.tracking:
            self.text = self.variable()

        if self.max_width:
            self.lines = [self.font.render(line.strip(), False, self.text_colour) for line in
                          self.get_lines(self.text, self.max_width)]
        else:
            self.lines = [self.font.render(self.text, False, self.text_colour)] if self.text else []

    def get_y(self):
        ys = max([line.get_height() for line in self.lines])
        return ys

    def get_x(self):
        xs = max([line.get_width() for line in self.lines])
        return xs

    def get_lines(self, t, max_width):
        if not t:
            return []

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
        self.update_text()  # can probably clean this up
        for y, line in enumerate(self.lines):
            if self.background:
                pygame.draw.rect(self.screen, self.background_colour,
                                 pygame.Rect(self.position[0], self.position[1] + self.size * y + 2 * self.padding * y,
                                             line.get_width() + self.padding * 2, line.get_height() + self.padding * 2),
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


def solve(cc=None):
    C = Cube(static=(300, 160), scaling=7, show_all=True, cc=cc, solve=True) if cc else Cube(static=(300, 160),
                                                                                             scaling=7,
                                                                                             show_all=True,
                                                                                             solve=True)

    step1 = Cube(static=(900, 300), scaling=5)
    step2 = Cube(static=(1300, 360), scaling=4)
    step3 = Cube(static=(1625, 420), scaling=3)

    running = True

    escape = TextButton(screen, (screen_width - 215, 20), "Escape", size=30, shadow_colour=(200, 0, 0))

    input_cube = TextButton(screen, (50, 980), "Input Cube", text_colour=(255, 255, 255), shadow_colour=(255, 0, 0))

    sol = Text(screen, "NOT SOLVED", (300, 800), background_colour=(0, 0, 0), tracking=True,
               track_target=C.get_solutions)

    solve_cube = TextButton(screen, (50, 880), "Solve", size=50, text_colour=(255, 255, 255), shadow_colour=(255, 0, 0),
                            functions=[C.solve])
    click = False

    drawable = [escape, C, solve_cube, input_cube, step1, step2, step3, sol]

    objects = [solve_cube]

    while running:
        clock.tick(400)

        screen.fill((40, 43, 48))

        mx, my = pygame.mouse.get_pos()

        if click:
            if escape.is_pressed(mx, my):
                running = False

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


def scramble(cc, length):
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
                 text_colour=(0, 255, 255))  # TODO something not working here - title not rendering

    s_pos = (50, title.position[1] + title.get_y() + title.padding * 2 + 20)
    s_size = 40
    s_bgcolour = (40, 43, 48)
    s_txtcolour = (0, 255, 255)

    s = Text(screen, "None", s_pos, size=s_size, background_colour=s_bgcolour, text_colour=s_txtcolour,
             max_width=900, tracking=True, track_target=cc.get_scramble)

    path = os.getcwd() + "\lib"
    cnt = Counter(24, lower_limit=1)

    n = Text(screen, str(cnt), (0, 876), background=False, size=80, tracking=True,
             track_target=cnt.get_size)  # not rendering this for some reason, no idea. It's probably default values in draw function again...

    barrow = ImageButton(screen, (50, 820), path + r"\arrows\barrow.png", scaling=15,
                         functions=[cnt.decrement, n.update_text])
    rarrow = ImageButton(screen, (500, 820), path + r"\arrows\rarrow.png", scaling=15,
                         rotation=180, functions=[cnt.increment, n.update_text])

    n.position = (((barrow.position[0] + barrow.image.get_width()) + (rarrow.position[0])) / 2 - (n.get_x() / 2), 876)

    clickable = [barrow, rarrow]

    objects = [scramble_cube, solve_cube, title, escape, barrow, rarrow, s, n]

    click = False

    while running:
        clock.tick(400)

        screen.fill((40, 43, 48))

        mx, my = pygame.mouse.get_pos()

        if click:

            if escape.is_pressed(mx, my):
                running = False

            elif scramble_cube.is_pressed(mx, my):
                cc = Cube(static=POS, scaling=SCALING)
                scramble(cc, int(cnt.get_size()))

            elif solve_cube.is_pressed(mx, my):
                solve(cc.cubiecube)
            #     # TODO implementation here

            for obj in clickable:
                if obj.is_pressed(mx, my):
                    obj.run()

        for obj in objects:  # draw out the objects
            obj.draw()

        cc.draw()

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
