from math import cos, sin

from constants import consts as c
from images import imgs as i
from trail import Trail


class Player:
    def __init__(self):
        self.image = i.player_ship
        self.width, self.height = self.image.get_size()

        self.global_x, self.global_y = 0, 0
        self.local_x, self.local_y = (c.s_width - self.width) // 2, (c.s_height - self.height) // 2
        self.angle = 0

    def update(self):
        self.dx, self.dy = 0, 0

        self.dx += c.player_move_speed * sin(self.angle) * c.dt
        self.dy += c.player_move_speed * cos(self.angle) * c.dt

        self.global_x += self.dx
        self.global_y += self.dy

        c.trails.append(Trail(self.global_x, self.global_y - self.height // 2))

    def render(self):
        c.screen.blit(self.image, (self.local_x, self.local_y))