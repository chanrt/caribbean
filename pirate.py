from math import cos, degrees, sin
from numpy import array
import pygame as pg

from constants import consts as c
from images import imgs as i


class Pirate:
    def __init__(self, position, angle):
        # sprite
        self.image = i.pirate_ship
        self.width, self.height = self.image.get_size()
        self.length_vector = array([self.width, self.height], dtype=float)

        # position and orientation
        self.global_position = position
        self.angle = angle
        self.steer_angle = 0

    def update(self):
        self.heading = array([sin(self.angle), cos(self.angle)], dtype=float)
        self.velocity = self.heading * c.pirate_move_speed

        # rotating image sprite
        if self.steer_angle != 0:
            self.image = pg.transform.rotate(i.player_ship, degrees(self.angle))
            self.width, self.height = self.image.get_size()
            self.length_vector[0], self.length_vector[1] = self.width, self.height

        # updating changes
        self.global_position += self.velocity * c.dt
        self.angle += self.steer_angle

        self.local_position = c.center_position + c.player.global_position - self.global_position - self.length_vector / 2

    def render(self):
        c.screen.blit(self.image, self.local_position)