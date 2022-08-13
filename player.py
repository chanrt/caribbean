from constants import consts as c
from images import imgs as i


class Player:
    def __init__(self):
        self.image = i.player_ship
        self.width, self.height = self.image.get_size()

        self.global_x, self.global_y = 0, 0
        self.local_x, self.local_y = (c.s_width - self.width) // 2, (c.s_height - self.height) // 2

    def render(self):
        c.screen.blit(self.image, (self.local_x, self.local_y))