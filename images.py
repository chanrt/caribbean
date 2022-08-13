import pygame as pg


class Images:
    def __init__(self):
        pg.display.init()
        self.player_ship = pg.transform.rotate(pg.image.load('sprites/player_ship.png'), 180)
        self.projectile = pg.image.load('sprites/projectile.png')

    def convert(self):
        self.player_ship = self.player_ship.convert_alpha()
        self.projectile = self.projectile.convert_alpha()


imgs = Images()