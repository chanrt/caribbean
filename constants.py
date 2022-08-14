from math import radians
import pygame as pg


class Constants:
    def __init__(self):
        # render params
        self.fps = 120
        self.dt = 1.0 / self.fps

        # colors
        self.water_color = pg.Color(9, 195, 219)
        self.island_color = pg.Color(0, 128, 0)

        # player speed params
        self.player_move_speed = 30
        self.player_turn_rate = radians(0.2)
        self.player_max_turn = radians(10)

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
        self.island_num_points = 30
        self.island_min_radius = 80
        self.island_max_radius = 100
        self.island_min_std = 5
        self.island_max_std = 10

    def set_screen(self, screen):
        self.screen = screen
        self.s_width, self.s_height = screen.get_size()

    def set_player(self, player):
        self.player = player

    def set_trails(self, trails):
        self.trails = trails

    def set_projectiles(self, projectiles):
        self.projectiles = projectiles

    def set_dt(self, dt):
        self.dt = dt


consts = Constants()