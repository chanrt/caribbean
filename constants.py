

class Constants:
    def __init__(self):
        pass

    def set_screen(self, screen):
        self.screen = screen
        self.s_width, self.s_height = screen.get_size()


consts = Constants()