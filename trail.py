from random import random
import pygame as pg

from constants import consts as c


class Trail:
    def __init__(self, x, y):
        self.global_x, self.global_y = x, y
        self.radius = c.trail_radius

    def update(self):
        self.global_x -= c.player.dx
        self.global_y -= c.player.dy

        self.local_x = c.s_width / 2 + c.player.global_x - self.global_x
        self.local_y = c.s_height / 2 + c.player.global_y - self.global_y

        if random() < c.trail_decay_probability and self.radius > 0:
            self.radius -= 1 

    def render(self):
        pg.draw.circle(c.screen, (255, 255, 255), (self.local_x, self.local_y), self.radius)