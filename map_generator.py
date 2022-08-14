from itertools import product
from numpy import floor
from random import randint

from constants import consts as c
from island import Island


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
            x = randint(x_min, x_max)
            y = randint(y_min, y_max)
            new_island = Island(x, y)
            c.add_island(new_island)

        # add to sectors mapped
        self.sectors_mapped.append(sector)

    def check_neighbouring_sectors(self):
        self.current_sector = floor(c.player.global_position / c.sector_length)

        for i_offset, j_offset in product([-1, 0, 1], [-1, 0, 1]):
            self.neighbouring_sector = [self.current_sector[0] + j_offset, self.current_sector[1] + i_offset]

            if self.neighbouring_sector not in self.sectors_mapped:
                self.map_sector(self.neighbouring_sector)
