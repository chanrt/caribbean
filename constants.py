from math import radians
from numpy import array
import pygame as pg


class Constants:
    def __init__(self):
        # render params
        self.garbage_collect = 60
        self.fps = 120
        self.dt = 1.0 / self.fps

        # colors
        self.water_color = pg.Color(9, 195, 219)
        self.sand_color = pg.Color(194, 178, 128)
        self.grass_color = pg.Color(0, 150, 0)

        # player speed params
        self.player_move_speed = 30
        self.player_turn_rate = radians(0.2)
        self.player_max_turn = radians(10)

        # pirate speed params
        self.pirate_move_speed = 30

        # player fire params
        self.player_num_broadside_shots = 6
        self.player_num_stern_shots = 2
        self.player_next_fire = 40
        self.player_broadside_cooldown = 3
        self.player_stern_cooldown = 1.5
        self.recoil = 1

        # projectile params
        self.projectile_speed = 200

        # trail params
        self.player_trail_cycle = 10
        self.trail_radius = 10
        self.trail_decay_probability = 0.02

        # island params
        self.island_num_points = 36
        self.island_min_radius = 80
        self.island_max_radius = 100
        self.island_min_std = 5
        self.island_max_std = 10
        self.island_inner_min = 0.5
        self.island_inner_max = 0.6

        # sector params
        self.sector_length = 700
        self.min_islands = 1
        self.max_islands = 3

    def set_screen(self, screen):
        self.screen = screen
        self.s_width, self.s_height = screen.get_size()
        self.center_position = array([self.s_width // 2, self.s_height // 2])

    def set_player(self, player):
        self.player = player

    def set_trails(self, trails):
        self.trails = trails

    def set_projectiles(self, projectiles):
        self.projectiles = projectiles

    def set_islands(self, islands):
        self.islands = islands

    def set_dt(self, dt):
        self.dt = dt
        self.fps = int(1.0 / dt)


consts = Constants()