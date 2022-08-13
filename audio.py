import pygame as pg


class Audio:
    def __init__(self):
        pg.mixer.init()
        self.shoot = pg.mixer.Sound('audio/shoot.wav')


aud = Audio()