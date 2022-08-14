import pygame as pg


class Audio:
    def __init__(self):
        pg.mixer.init()
        self.broadside_fire = pg.mixer.Sound('sounds/broadside_fire.wav')
        self.stern_fire = pg.mixer.Sound('sounds/stern_fire.wav')


aud = Audio()