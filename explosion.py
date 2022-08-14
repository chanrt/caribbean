import pygame as pg

from constants import consts as c
from images import imgs as i


class Explosion:
    def __init__(self, x, y):
        self.images = i.explosion
        self.width, self.height = self.images[0].get_size()
        self.global_x, self.global_y = x, y
        self.cycle = -1
        self.update()

    def update(self):
        self.global_x -= c.player.dx
        self.global_y -= c.player.dy

        self.local_x = c.s_width / 2 + c.player.global_x - self.global_x - self.width / 2
        self.local_y = c.s_height / 2 + c.player.global_y - self.global_y - self.height / 2

        self.cycle += 1

    def render(self):
        if self.cycle < len(self.images):
            c.screen.blit(self.images[self.cycle], (self.local_x, self.local_y))
