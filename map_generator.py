from itertools import product
from math import pi
from numpy import array, floor
from random import random, randint

from constants import consts as c
from island import Island
from pirate import Pirate
from utils import *


class MapGenerator:
    def __init__(self):
        self.sectors_mapped = []

    def map_sector(self, sector):
        # compute extent
        x_min, y_min = sector[0] * c.sector_length, sector[1] * c.sector_length
        x_max, y_max = x_min + c.sector_length, y_min + c.sector_length

        # add islands
        num_islands = randint(c.min_islands, c.max_islands)
        for _ in range(num_islands):
            while True:
                x = randint(x_min, x_max)
                y = randint(y_min, y_max)

                new_island = Island(x, y)
                no_problem = True

                if global_distance_between(new_island, c.player) < c.sector_length / 2:
                    no_problem = False
                if no_problem:
                    for pirate in c.pirates:
                        if global_distance_between(pirate, new_island) < c.sector_length / 2:
                            no_problem = False
                            break

                if no_problem:
                    c.add_island(new_island)
                    break

        # add pirates
        for _ in range(c.num_pirates):
            while True:
                x = randint(x_min, x_max)
                y = randint(y_min, y_max)
                angle = random() * 2 * pi - pi

                new_pirate = Pirate(array([x, y], dtype=float), angle)
                no_problem = True

                if global_distance_between(new_pirate, c.player) < c.sector_length / 2:
                    no_problem = False
                if no_problem:
                    for island in c.islands:
                        if global_distance_between(island, new_pirate) < c.sector_length / 2:
                            no_problem = False
                            break

                if no_problem:
                    c.add_pirate(new_pirate)
                    break

        # add to sectors mapped
        self.sectors_mapped.append(sector)

    def check_neighbouring_sectors(self):
        self.current_sector = floor(c.player.global_position / c.sector_length)

        for i_offset, j_offset in product([-1, 0, 1], [-1, 0, 1]):
            self.neighbouring_sector = [self.current_sector[0] + j_offset, self.current_sector[1] + i_offset]

            if self.neighbouring_sector not in self.sectors_mapped:
                self.map_sector(self.neighbouring_sector)
