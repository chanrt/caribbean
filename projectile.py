from math import cos, sin
from numpy import array

from constants import consts as c
from images import imgs as i

class Projectile:
    def __init__(self, position, angle, origin):
        # sprite
        self.image = i.projectile
        self.width, self.height = self.image.get_size()
        self.length_vector = array([self.width, self.height], dtype=float)
        self.origin = origin

        # position and velocity
        self.global_position = position
        heading = array([sin(angle), cos(angle)], dtype=float)
        self.velocity = c.projectile_speed * heading + c.player.velocity

        # flags
        self.inside_screen = True
        self.destroyed = False

    def update(self):
        self.global_position += self.velocity * c.dt
        self.local_position = c.center_position + c.player.global_position - self.global_position - self.length_vector / 2

        if (0 < self.local_position[0] < c.s_width) and (0 < self.local_position[1] < c.s_height):
            self.inside_screen = True
        else:
            self.inside_screen = False

    def render(self):
        c.screen.blit(i.projectile, self.local_position)

    def destroy(self):
        self.destroyed = True