import pygame as pg


class Constants:
    def __init__(self):
        self.fps = 30
        self.dt = 1.0 / self.fps

        self.water_color = pg.Color(9, 195, 219)

        self.player_move_speed = 30

        self.trail_radius = 10
        self.trail_decay_probability = 0.025

    def set_screen(self, screen):
        self.screen = screen
        self.s_width, self.s_height = screen.get_size()

    def set_player(self, player):
        self.player = player

    def set_trails(self, trails):
        self.trails = trails

    def set_dt(self, dt):
        self.dt = dt


consts = Constants()