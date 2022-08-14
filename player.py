from math import cos, degrees, pi, sin
import pygame as pg

from audio import aud as a
from constants import consts as c
from images import imgs as i
from projectile import Projectile
from trail import Trail


class Player:
    def __init__(self):
        # sprite
        self.image = i.player_ship
        self.image_rect = self.image.get_rect(center=(c.s_width // 2, c.s_height // 2))
        self.width, self.height = self.image.get_size()

        # position and orientation
        self.global_x, self.global_y = 0, 0
        self.angle = 0
        self.steer_angle = 0

        # broadside 
        self.broadside_fire_cycle = 0
        self.broadside_firing = False
        self.broadside_fire_dir = 0
        self.broadside_next_fire = 0

    def update(self, keys_pressed):
        self.dx, self.dy = 0, 0

        # movement
        self.dx += c.player_move_speed * sin(self.angle) * c.dt
        self.dy += c.player_move_speed * cos(self.angle) * c.dt

        # steering
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

        # updating changes
        self.global_x += self.dx
        self.global_y += self.dy
        self.angle += self.steer_angle

        # rotating image sprite
        if self.steer_angle != 0:
            self.image = pg.transform.rotate(i.player_ship, degrees(self.angle))
            self.image_rect = self.image.get_rect(center=(c.s_width // 2, c.s_height // 2))
            self.width, self.height = self.image.get_size()

        # generate trail
        new_trail = Trail(self.global_x - sin(self.angle) * self.width / 2, self.global_y - cos(self.angle) * self.height / 2)
        c.trails.append(new_trail)

        # checking broadside fire
        if self.broadside_firing:
            if self.broadside_next_fire == 0:
                self.fire_broadside()
                a.shoot.play()

                self.broadside_next_fire += 1
                self.broadside_fire_cycle += 1

                if self.broadside_fire_cycle == c.player_broadside_fire_cycle:
                    self.broadside_firing = False
                    self.broadside_fire_cycle = 0
            else:
                self.broadside_next_fire += 1
                if self.broadside_next_fire == c.player_broadside_next_fire:
                    self.broadside_next_fire = 0

    def render(self):
        c.screen.blit(self.image, self.image_rect)

    def fire_broadside(self):
        # bow location
        self.front_x = self.global_x + sin(self.angle) * self.width / 2
        self.front_y = self.global_y + cos(self.angle) * self.height / 2

        # stern location
        self.back_x = self.global_x - sin(self.angle) * self.width / 2
        self.back_y = self.global_y - cos(self.angle) * self.height / 2

        # decide projectile coords and direction
        interpolation = (self.broadside_fire_cycle + 1) / (c.player_broadside_fire_cycle + 1)
        start_x = self.front_x + interpolation * (self.back_x - self.front_x)
        start_y = self.front_y + interpolation * (self.back_y - self.front_y)
        angle = self.angle + self.broadside_fire_dir * pi / 2

        # generate projectile
        new_projectile = Projectile(start_x, start_y, angle, "player")
        c.projectiles.append(new_projectile)

    def prepare_broadside_fire(self, direction):
        if not self.broadside_firing:
            self.broadside_firing = True
            self.broadside_fire_dir = direction
            self.broadside_fire_cycle = 0