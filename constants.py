from math import radians
from numpy import array
import pygame as pg


class Constants:
    def __init__(self):
        # render params
        self.garbage_collect = 60
        self.fps = 120
        self.dt = 1.0 / self.fps

        # object lists
        self.all_objects = []
        self.islands = []
        self.pirates = []

        # colors
        self.water_color = pg.Color(9, 195, 219)
        self.sand_color = pg.Color(194, 178, 128)
        self.grass_color = pg.Color(0, 150, 0)

        # player speed params
        self.player_move_speed = 30
        self.player_turn_speed = radians(20)

        # pirate speed params
        self.pirate_move_speed = 30
        self.pirate_turn_speed = radians(20)

        # flocking params
        self.repulsion_radius = 200
        self.orientation_radius = 400
        self.attraction_radius = 600

        # player fire params
        self.player_num_broadside_shots = 6
        self.player_num_stern_shots = 2
        self.next_fire_cooldown_time = 0.25
        self.broadside_cooldown_time = 3
        self.stern_cooldown_time = 1.5
        self.pirate_fire_cooldown = 1
        self.recoil = 1

        # projectile params
        self.projectile_speed = 200

        # trail params
        self.full_trail_cycle = 10
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
        self.sector_length = 800
        self.min_islands = 1
        self.max_islands = 2
        self.num_pirates = 1

        # explosion
        self.explosion_rate = 0.33

        # leeways
        self.pirate_leeway = 113

        # font
        pg.init()
        self.font = pg.font.SysFont("arial", 25)

    def set_screen(self, screen):
        self.screen = screen
        self.s_width, self.s_height = screen.get_size()
        self.center_position = array([self.s_width // 2, self.s_height // 2])

    def set_player(self, player):
        self.player = player
        self.all_objects.append(player)

    def set_trails(self, trails):
        self.trails = trails

    def set_projectiles(self, projectiles):
        self.projectiles = projectiles

    def set_dt(self, dt):
        self.dt = dt
        self.fps = int(1.0 / dt)

    def add_island(self, island):
        self.islands.append(island)
        self.all_objects.append(island)

    def add_pirate(self, pirate):
        self.pirates.append(pirate)
        self.all_objects.append(pirate)

    def remove_pirate(self, pirate):
        self.pirates.remove(pirate)
        self.all_objects.remove(pirate)


consts = Constants()