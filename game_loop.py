from time import time
import pygame as pg

from constants import consts as c
from player import Player


def game_loop(screen):
    pg.display.set_caption("Caribbean")

    player = Player()
    c.set_player(player)

    trails = []
    c.set_trails(trails)

    while True:
        start = time()

        keys_pressed = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return

        screen.fill(c.water_color)

        player.update(keys_pressed)
        for trail in trails:
            trail.update()

        for trail in trails:
            trail.render()
        player.render()

        pg.display.flip()

        end = time()
        c.set_dt(end - start)


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen(screen)
    game_loop(screen)