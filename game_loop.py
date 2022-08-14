from matplotlib import path
from time import time
import pygame as pg

from constants import consts as c
from island import Island
from player import Player


def game_loop(screen):
    pg.display.set_caption("Caribbean")

    player = Player()
    c.set_player(player)

    trails = []
    c.set_trails(trails)

    projectiles = []
    c.set_projectiles(projectiles)

    islands = []
    island = Island(0, 500)
    islands.append(island)

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
        player.update(keys_pressed)
        for island in islands:
            island.update()
        for trail in trails:
            trail.update()
        for projectile in projectiles:
            projectile.update()

        # check for collisions
        for island in islands:
            polygon = path.Path(island.global_points)
            inside = polygon.contains_points(player.reference_points)
            if any(inside):
                return

        # renders
        for trail in trails:
            trail.render()
        for island in islands:
            if island.inside_screen:
                island.render()
        for projectile in projectiles:
            projectile.render()
        player.render()

        pg.display.flip()

        end = time()
        c.set_dt(end - start)

        # garbage collection
        frame += 1
        if frame == c.fps:
            frame = 0

            # clear decayed trails
            trails = [trail for trail in trails if trail.radius > 0]
            c.set_trails(trails)

            # clear decayed projectiles
            projectiles = [projectile for projectile in projectiles if projectile.inside_screen()]
            c.set_projectiles(projectiles)


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    # screen = pg.display.set_mode((800, 600))
    c.set_screen(screen)
    game_loop(screen)