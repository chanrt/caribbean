import pygame as pg


def serialize_images(image, num_horizontal, num_vertical, width, height):
    cropped_images = []

    for i in range(0, num_vertical):
        for j in range(0, num_horizontal):
            cropped_image = pg.Surface((width, height), pg.SRCALPHA)
            cropped_image.blit(image, (0, 0), (j * width, i * height, width, height))
            cropped_images.append(cropped_image)

    return cropped_images


class Images:
    def __init__(self):
        pg.display.init()
        self.player_ship = pg.transform.rotate(pg.image.load('sprites/player_ship.png'), 180)
        self.projectile = pg.image.load('sprites/projectile.png')
        self.explosion_sprite = pg.image.load('sprites/explosion.png')
        self.explosion = serialize_images(self.explosion_sprite, 5, 5, 100, 100)

    def convert(self):
        self.player_ship = self.player_ship.convert_alpha()
        self.projectile = self.projectile.convert_alpha()
        self.explosion = [image.convert_alpha() for image in self.explosion]


imgs = Images()


if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((100, 100))
    clock = pg.time.Clock()

    frame = 0

    while True:
        clock.tick(5)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        
        screen.fill((0, 0, 0))
        print(frame)
        screen.blit(imgs.explosion[frame], (0, 0))

        frame += 1
        if frame == len(imgs.explosion):
            frame = 0

        pg.display.flip()