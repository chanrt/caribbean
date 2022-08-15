from math import atan2, cos, degrees, pi, sin
from numpy import array, linalg, zeros
import pygame as pg

from constants import consts as c
from images import imgs as i
from trail import Trail
from utils import *


class Pirate:
    def __init__(self, position, angle):
        # sprite
        self.image = pg.transform.rotate(i.pirate_ship, degrees(angle))
        self.width, self.height = self.image.get_size()
        self.length_vector = array([self.width, self.height], dtype=float)

        # position and orientation
        self.global_position = position
        self.angle = angle
        self.heading = array([sin(self.angle), cos(self.angle)], dtype=float)
        self.steer_angle = 0

        self.front_position = self.global_position + self.heading * self.length_vector / 2
        self.back_position = self.global_position - self.heading * self.length_vector / 2
        self.reference_points = [self.front_position, self.back_position]

        # trail
        self.trail_cycle = 0

        # flags
        self.destroyed = False
        self.inside_screen = False
        self.angle_changed = False

    def update(self):
        self.local_position = c.center_position + c.player.global_position - self.global_position - self.length_vector / 2
        
        if inside_screen(self, "pirate"):
            self.inside_screen = True
        else:
            self.inside_screen = False

        if self.inside_screen:
            self.heading = array([sin(self.angle), cos(self.angle)], dtype=float)
            self.velocity = self.heading * c.pirate_move_speed

            self.get_repelling_objects()
            if len(self.repelling_objects) > 0:
                # print(self.repelling_objects)
                repulsion_sum = zeros(2, dtype=float)
                for obj in self.repelling_objects:
                    repelling_vector = obj.global_position - self.global_position
                    repelling_vector /= linalg.norm(repelling_vector)
                    repulsion_sum += repelling_vector

                # act as if something is behind the ship too
                # repelling_vector = self.back_position - self.global_position
                # repelling_vector /= linalg.norm(repelling_vector)
                # repulsion_sum += repelling_vector

                repulsion_sum *= -1
                # print(repulsion_sum)
                self.set_velocity(repulsion_sum)

            if self.angle_changed:
                self.image = pg.transform.rotate(i.pirate_ship, degrees(self.angle))
                self.width, self.height = self.image.get_size()
                self.length_vector[0], self.length_vector[1] = self.width, self.height
                self.angle_changed = False

            # updating changes
            self.global_position += self.velocity * c.dt
            self.local_position = c.center_position + c.player.global_position - self.global_position - self.length_vector / 2

            while self.angle < -pi:
                self.angle += 2 * pi
            while self.angle > pi:
                self.angle -= 2 * pi

            self.front_position = self.global_position + self.heading * self.length_vector / 2
            self.back_position = self.global_position - self.heading * self.length_vector / 2
            self.reference_points = [self.front_position, self.back_position]

            self.trail_cycle += 1
            if self.trail_cycle == c.full_trail_cycle:
                self.trail_cycle = 0
                new_trail = Trail(self.back_position)
                c.trails.append(new_trail)

    def render(self):
        if self.inside_screen:
            c.screen.blit(self.image, self.local_position)

    def set_velocity(self, req_velocity):
        req_angle = atan2(req_velocity[0], req_velocity[1])

        if abs(req_angle - self.angle) < c.pirate_turn_speed * c.dt:
            self.angle = req_angle
            self.angle_changed = True
        else:
            if req_angle < self.angle:
                if abs(req_angle - self.angle) < pi:
                    # print("turning right")
                    self.angle -= c.pirate_turn_speed * c.dt
                    self.angle_changed = True
                else:
                    # print("turning left")
                    self.angle += c.pirate_turn_speed * c.dt
                    self.angle_changed = True
            else:
                if abs(req_angle - self.angle) < pi:
                    # print("turning left")
                    self.angle += c.pirate_turn_speed * c.dt
                    self.angle_changed = True
                else:
                    # print("turning right")
                    self.angle -= c.pirate_turn_speed * c.dt
                    self.angle_changed = True

    def get_repelling_objects(self):
        self.repelling_objects = []

        for obj in c.all_objects:
            if obj != self:
                distance = global_distance_between(self, obj)
                if distance < c.repulsion_radius:
                    self.repelling_objects.append(obj)

    def destroy(self):
        self.destroyed = True