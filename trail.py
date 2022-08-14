from random import random
import pygame as pg

from constants import consts as c


class Trail:
    def __init__(self, position):
        self.global_position = position
        self.radius = c.trail_radius

    def update(self):
        self.global_position -= c.player.velocity * c.dt
        self.local_position = c.center_position + c.player.global_position - self.global_position

        if random() < c.trail_decay_probability and self.radius > 0:
            self.radius -= 1 

    def render(self):
        pg.draw.circle(c.screen, (255, 255, 255), self.local_position, self.radius)