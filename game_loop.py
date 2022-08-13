import pygame as pg
from constants import consts as c
from player import Player


def game_loop(screen):
    pg.display.set_caption("Caribbean")
    bg_color = pg.Color("blue")

    player = Player()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return

        screen.fill(bg_color)

        player.render()

        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    c.set_screen(screen)
    game_loop(screen)