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
        self.outer_polygon = []
        outer_radii = random.normal(mean_radius, mean_std, c.island_num_points)
        thetas = linspace(0, 2 * pi, c.island_num_points)
        for r, theta in zip(outer_radii, thetas):
            self.outer_polygon.append((r * cos(theta), r * sin(theta)))

        self.inner_polygon = []
        ratios = random.uniform(0.4, 0.8, c.island_num_points)
        for ratio, r, theta in zip(ratios, outer_radii, thetas):
            self.inner_polygon.append((ratio * r * cos(theta), ratio * r * sin(theta)))

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

        if self.inside_screen:
            self.global_outer_points = [(self.global_x + x, self.global_y + y) for x, y in self.outer_polygon]
            self.local_outer_points = [(self.local_x + x, self.local_y + y) for x, y in self.outer_polygon]
            self.local_inner_points = [(self.local_x + x, self.local_y + y) for x, y in self.inner_polygon]

    def render(self):
        if self.inside_screen:
            pg.draw.polygon(c.screen, c.sand_color, self.local_outer_points)
            pg.draw.polygon(c.screen, c.grass_color, self.local_inner_points)