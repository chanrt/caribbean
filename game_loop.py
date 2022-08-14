from matplotlib import path
from time import time
import pygame as pg

from constants import consts as c
from explosion import Explosion
from images import imgs as i
from island import Island
from map_generator import MapGenerator
from pirate import Pirate
from player import Player
from utils import *


def game_loop(screen):
    pg.display.set_caption("Caribbean")
    clock = pg.time.Clock()
    i.convert()

    player = Player()
    c.set_player(player)

    trails = []
    c.set_trails(trails)

    projectiles = []
    c.set_projectiles(projectiles)

    islands = []
    c.set_islands(islands)

    pirates = []
    # pirate = Pirate([0, 200], 0)
    # pirates.append(pirate)

    map_generator = MapGenerator()
    map_generator.check_neighbouring_sectors()

    for island in islands:
        distance = global_distance_between(player, island)
        if distance < c.sector_length:
            islands.remove(island)

    explosions = []

    frame = 0

    while True:
        start = time()

        # inputs
        keys_pressed = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return
                if event.key == pg.K_q:
                    # fire portside cannons
                    player.prepare_fire(1)
                if event.key == pg.K_w:
                    # fire stern cannons
                    player.prepare_fire(0)
                if event.key == pg.K_e:
                    # fire starboard cannons
                    player.prepare_fire(-1)

        screen.fill(c.water_color)

        # updates
        if not player.destroyed:
            player.update(keys_pressed)
        for island in islands:
            island.update()
        for trail in trails:
            trail.update()
        for projectile in projectiles:
            projectile.update()
        for explosion in explosions:
            explosion.update()
        for pirate in pirates:
            pirate.update()

        # collision between player and islands
        if not player.destroyed:
            for island in islands:
                if island.inside_screen:
                    polygon = path.Path(island.global_outer_points)
                    inside = polygon.contains_points(player.reference_points)
                    if any(inside):
                        player.destroy()
                        explosion = Explosion(player.global_position)
                        explosions.append(explosion)

        # collision between projectiles and islands
        for projectile in projectiles:
            for island in islands:
                distance = global_distance_between(projectile, island)
                if distance < island.mean_radius:
                    projectile.destroy()

        # renders
        for trail in trails:
            trail.render()
        for island in islands:
            island.render_outer()
        for island in islands:
            island.render_inner()
        for projectile in projectiles:
            projectile.render()
        for explosion in explosions:
            explosion.render()
        for pirate in pirates:
            pirate.render()
        if not player.destroyed:
            player.render()

        pg.display.flip()

        end = time()
        c.set_dt(end - start)
        # print(c.fps)

        # garbage collection and non important tasks
        frame += 1
        if frame == c.garbage_collect:
            frame = 0

            # clear decayed trails
            trails = [trail for trail in trails if trail.radius > 0]
            c.set_trails(trails)

            # clear decayed projectiles
            projectiles = [projectile for projectile in projectiles if projectile.inside_screen and not projectile.destroyed]
            c.set_projectiles(projectiles)

            # check for unmapped neighbouring sectors
            # map_generator.check_neighbouring_sectors()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    # screen = pg.display.set_mode((800, 600))
    c.set_screen(screen)
    game_loop(screen)