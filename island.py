from math import cos, pi, sin
from numpy import linspace, random
from random import randint
import pygame as pg

from constants import consts as c


class Island:
    def __init__(self, x, y):
        # position
        self.global_x, self.global_y = x, y

        # size params
        mean_radius = randint(c.island_min_radius, c.island_max_radius)
        mean_std = randint(c.island_min_std, c.island_max_std)

        # generate points
        self.polygon = []
        radii = random.normal(mean_radius, mean_std, c.island_num_points)
        thetas = linspace(0, 2 * pi, c.island_num_points)
        for r, theta in zip(radii, thetas):
            self.polygon.append((r * cos(theta), r * sin(theta)))

        # flags
        self.inside_screen = False

    def update(self):
        self.global_x -= c.player.dx
        self.global_y -= c.player.dy

        self.local_x = c.s_width / 2 + c.player.global_x - self.global_x
        self.local_y = c.s_height / 2 + c.player.global_y - self.global_y

        if -c.island_max_radius < self.local_x < c.s_width + c.island_max_radius and -c.island_max_radius < self.local_y < c.s_height + c.island_max_radius:
            self.inside_screen = True
        else:
            self.inside_screen = False

    def render(self):
        points = [(self.local_x + x, self.local_y + y) for x, y in self.polygon]
        pg.draw.polygon(c.screen, (255, 255, 255), points)