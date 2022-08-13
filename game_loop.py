import pygame as pg


def game_loop(screen):
    bg_color = pg.Color("blue")

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return

        screen.fill(bg_color)
        pg.display.flip()