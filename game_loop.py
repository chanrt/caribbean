from time import time
import pygame as pg

from constants import consts as c
from images import imgs as i
from player import Player


def game_loop(screen):
    pg.display.set_caption("Caribbean")

    player = Player()
    c.set_player(player)

    trails = []
    c.set_trails(trails)

    projectiles = []
    c.set_projectiles(projectiles)

    frame = 0

    while True:
        # clock.tick(c.fps)
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
                    player.prepare_fire(1)
                if event.key == pg.K_e:
                    player.prepare_fire(-1)

        screen.fill(c.water_color)

        # updates
        player.update(keys_pressed)
        for trail in trails:
            trail.update()
        for projectile in projectiles:
            projectile.update()

        # renders
        for trail in trails:
            trail.render()
        for projectile in projectiles:
            projectile.render()
        player.render()

        pg.display.flip()

        end = time()
        c.set_dt(end - start)

        frame += 1
        if frame == c.fps:
            frame = 0

            # clear decayed trails
            trails = [trail for trail in trails if trail.radius > 0]
            c.set_trails(trails)


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen(screen)
    game_loop(screen)