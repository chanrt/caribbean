from math import cos, degrees, pi, sin
from numpy import array, zeros
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
        self.length_vector = array([self.width, self.height], dtype=float)

        # position and orientation
        self.global_position = zeros(2, dtype=float)
        self.angle = 0
        self.steer_angle = 0

        # fire params
        self.fire_cycle = 0
        self.firing = False
        self.fire_dir = 0

        # cooldowns
        self.next_fire_cooldown = 0
        self.portside_cooldown = 0
        self.stern_cooldown = 0
        self.starboard_cooldown = 0

        # trail
        self.trail_cycle = 0

        # flags
        self.destroyed = False
        self.angle_changed = True

    def update(self, keys_pressed):
        self.velocity = zeros(2, dtype=float)
        self.steer_angle = 0
        
        self.heading = array([sin(self.angle), cos(self.angle)], dtype=float)
        self.velocity += self.heading * c.player_move_speed

        # steering
        if (keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_a]):
            self.steer_angle += c.player_turn_speed
            self.angle_changed = True
        if (keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_d]):
            self.steer_angle -= c.player_turn_speed
            self.angle_changed = True

        # updating changes
        self.global_position += self.velocity * c.dt
        self.angle += self.steer_angle * c.dt

        # rotating image sprite
        if self.angle_changed != 0:
            self.image = pg.transform.rotate(i.player_ship, degrees(self.angle))
            self.image_rect = self.image.get_rect(center=c.center_position)
            self.width, self.height = self.image.get_size()
            self.length_vector[0], self.length_vector[1] = self.width, self.height
            self.angle_changed = False

        # checking if firing
        if self.firing:
            if self.next_fire_cooldown == 0:
                self.fire()

                # play sound
                if self.fire_dir == 0:
                    a.stern_fire.play()
                else:
                    a.broadside_fire.play()
                    self.recoil()

                # advance fire cycles
                self.next_fire_cooldown += c.dt
                self.fire_cycle += 1

                if self.fire_dir == 0:
                    # stop stern fire
                    if self.fire_cycle == c.player_num_stern_shots:
                        self.firing = False
                        self.fire_cycle = 0
                        self.stern_cooldown = c.stern_cooldown_time
                else:
                    # stop broadside fire
                    if self.fire_cycle == c.player_num_broadside_shots:
                        self.firing = False
                        self.fire_cycle = 0

                        if self.fire_dir == 1:
                            self.portside_cooldown = c.broadside_cooldown_time
                        else:
                            self.starboard_cooldown = c.broadside_cooldown_time
            else:
                # advance intra-fire cycle
                self.next_fire_cooldown += c.dt
                if self.next_fire_cooldown > c.next_fire_cooldown_time:
                    self.next_fire_cooldown = 0

        # cooldowns
        if self.stern_cooldown > 0:
            self.stern_cooldown -= c.dt
            if self.stern_cooldown < 0:
                self.stern_cooldown = 0
        if self.portside_cooldown > 0:
            self.portside_cooldown -= c.dt
            if self.portside_cooldown < 0:
                self.portside_cooldown = 0
        if self.starboard_cooldown > 0:
            self.starboard_cooldown -= c.dt
            if self.starboard_cooldown < 0:
                self.starboard_cooldown = 0

        # updating reference points
        self.front_position = self.global_position + self.heading * self.length_vector / 2
        self.back_position = self.global_position - self.heading * self.length_vector / 2

        self.reference_points = [self.front_position, self.back_position]

        # generate trail
        self.trail_cycle += 1
        if self.trail_cycle == c.full_trail_cycle:
            self.trail_cycle = 0
            new_trail = Trail(self.back_position)
            c.trails.append(new_trail)

        # print(self.velocity)
        # print(degrees(self.angle))

    def render(self):
        c.screen.blit(self.image, self.image_rect)

    def fire(self):
        # decide projectile coords and direction
        if self.fire_dir == 0:
            stern_projectile = Projectile(self.front_position, self.angle, self)
            c.projectiles.append(stern_projectile)
        else:
            interpolation = (self.fire_cycle + 1) / (c.player_num_broadside_shots + 1)
            start_position = self.front_position + interpolation * (self.back_position - self.front_position)
            angle = self.angle + self.fire_dir * pi / 2

            broadside_projectile = Projectile(start_position, angle, self)
            c.projectiles.append(broadside_projectile)

    def recoil(self):
        recoil_vector = array([-cos(self.angle), sin(self.angle)])
        self.velocity += self.fire_dir * c.recoil * recoil_vector

    def ready_to_fire(self, direction):
        if direction == 0:
            return self.stern_cooldown == 0
        elif direction == 1:
            return self.portside_cooldown == 0
        else:
            return self.starboard_cooldown == 0

    def prepare_fire(self, direction):
        if not self.firing and self.ready_to_fire(direction):
            self.firing = True
            self.fire_dir = direction
            self.fire_cycle = 0

    def destroy(self):
        self.destroyed = True
        self.velocity[0], self.velocity[1] = 0, 0
        self.steer_angle = 0