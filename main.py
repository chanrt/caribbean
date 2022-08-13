import pygame as pg

from game_loop import game_loop


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    game_loop(screen)