from math import cos, sin

from constants import consts as c
from images import imgs as i

class Projectile:
    def __init__(self, x, y, angle):
        self.image = i.projectile
        self.width, self.height = self.image.get_size()

        self.global_x, self.global_y = x, y
        self.vx = c.projectile_speed * sin(angle) + c.player_move_speed * sin(c.player.angle)
        self.vy = c.projectile_speed * cos(angle) + c.player_move_speed * cos(c.player.angle)

    def update(self):
        self.global_x += self.vx * c.dt
        self.global_y += self.vy * c.dt

        self.local_x = c.s_width / 2 + c.player.global_x - self.global_x - self.width / 2
        self.local_y = c.s_height / 2 + c.player.global_y - self.global_y - self.height / 2

    def render(self):
        c.screen.blit(i.projectile, (self.local_x, self.local_y))