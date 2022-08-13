import pygame as pg


class Images:
    def __init__(self):
        self.player_ship = pg.transform.rotate(pg.image.load("sprites/player_ship.png"), 180)


imgs = Images()