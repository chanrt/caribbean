from numpy import array
import pygame as pg

from constants import consts as c
from images import imgs as i


class Explosion:
    def __init__(self, position):
        self.images = i.explosion
        self.width, self.height = self.images[0].get_size()
        self.length_vector = array([self.width, self.height], dtype=float)

        self.global_position = position
        self.cycle = -1
        self.update()

    def update(self):
        self.local_position = c.center_position + c.player.global_position - self.global_position - self.length_vector / 2
        self.cycle += 1

    def render(self):
        if self.cycle < len(self.images):
            c.screen.blit(self.images[self.cycle], self.local_position)
