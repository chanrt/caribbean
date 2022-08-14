from matplotlib import path
from time import time
import pygame as pg

from constants import consts as c
from explosion import Explosion
from images import imgs as i
from island import Island
from player import Player


def game_loop(screen):
    pg.display.set_caption("Caribbean")
    clock = pg.time.Clock()

    player = Player()
    c.set_player(player)

    trails = []
    c.set_trails(trails)

    projectiles = []
    c.set_projectiles(projectiles)

    islands = []
    island = Island(0, 500)
    islands.append(island)

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

        # check for collision between player and islands
        if not player.destroyed:
            for island in islands:
                polygon = path.Path(island.global_outer_points)
                inside = polygon.contains_points(player.reference_points)
                if any(inside):
                    player.destroy()
                    explosion = Explosion(player.global_x, player.global_y)
                    explosions.append(explosion)

        # renders
        for trail in trails:
            trail.render()
        for island in islands:
            if island.inside_screen:
                island.render()
        for projectile in projectiles:
            projectile.render()
        for explosion in explosions:
            explosion.render()
        if not player.destroyed:
            player.render()

        pg.display.flip()

        end = time()
        c.set_dt(end - start)
        # print(c.fps)

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
    i.convert()
    c.set_screen(screen)
    game_loop(screen)