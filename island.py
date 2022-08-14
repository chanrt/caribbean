from math import cos, pi, sin
from numpy import array, linspace, random
from random import randint
import pygame as pg

from constants import consts as c


class Island:
    def __init__(self, x, y):
        # position
        self.global_position = array([x, y], dtype=float)

        # size params
        self.mean_radius = randint(c.island_min_radius, c.island_max_radius)
        self.mean_std = randint(c.island_min_std, c.island_max_std)

        # generate points
        self.outer_polygon = []
        outer_radii = random.normal(self.mean_radius, self.mean_std, c.island_num_points)
        thetas = linspace(0, 2 * pi, c.island_num_points)
        for r, theta in zip(outer_radii, thetas):
            relative_position = array([r * cos(theta), r * sin(theta)], dtype=float)
            self.outer_polygon.append(relative_position)

        self.inner_polygon = []
        ratios = random.uniform(c.island_inner_min, c.island_inner_max, c.island_num_points)
        for ratio, r, theta in zip(ratios, outer_radii, thetas):
            relative_position = array([ratio * r * cos(theta), ratio * r * sin(theta)], dtype=float)
            self.inner_polygon.append(relative_position)

        # flags
        self.inside_screen = False

    def update(self):
        self.global_position -= c.player.velocity * c.dt
        self.local_position = c.center_position + c.player.global_position - self.global_position

        if -c.island_max_radius < self.local_position[0] < c.s_width + c.island_max_radius and -c.island_max_radius < self.local_position[1] < c.s_height + c.island_max_radius:
            self.inside_screen = True
        else:
            self.inside_screen = False

        if self.inside_screen:
            self.global_outer_points = [self.global_position + relative_position for relative_position in self.outer_polygon]
            self.local_outer_points = [self.local_position + relative_position for relative_position in self.outer_polygon]
            self.local_inner_points = [self.local_position + relative_position for relative_position in self.inner_polygon]

    def render(self):
        if self.inside_screen:
            pg.draw.polygon(c.screen, c.sand_color, self.local_outer_points)
            pg.draw.polygon(c.screen, c.grass_color, self.local_inner_points)