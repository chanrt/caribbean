from math import cos, degrees, sin
import pygame as pg

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
        self.steer_angle = 0

    def update(self, keys_pressed):
        self.dx, self.dy = 0, 0

        self.dx += c.player_move_speed * sin(self.angle) * c.dt
        self.dy += c.player_move_speed * cos(self.angle) * c.dt

        if (keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]) and abs(self.steer_angle) < c.player_max_turn * c.dt:
            self.steer_angle += c.player_turn_rate * c.dt
        if (keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]) and abs(self.steer_angle) < c.player_max_turn * c.dt:
            self.steer_angle -= c.player_turn_rate * c.dt
        if not keys_pressed[pg.K_LEFT] and not keys_pressed[pg.K_RIGHT] and not keys_pressed[pg.K_a] and not keys_pressed[pg.K_d]:
            if abs(self.steer_angle) < c.player_turn_rate * c.dt:
                self.steer_angle = 0
            elif self.steer_angle > 0:
                self.steer_angle -= c.player_turn_rate * c.dt
            else:
                self.steer_angle += c.player_turn_rate * c.dt

        self.global_x += self.dx
        self.global_y += self.dy
        self.angle += self.steer_angle

        if self.steer_angle != 0:
            self.image = pg.transform.rotate(i.player_ship, degrees(self.angle))
            self.width, self.height = self.image.get_size()
            self.local_x, self.local_y = (c.s_width - self.width) // 2, (c.s_height - self.height) // 2

        new_trail = Trail(self.global_x - sin(self.angle) * self.width / 2, self.global_y - cos(self.angle) * self.height / 2)
        c.trails.append(new_trail)

    def render(self):
        c.screen.blit(self.image, (self.local_x, self.local_y))