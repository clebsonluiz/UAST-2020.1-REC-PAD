import pygame as pg
import sys


def events(game):
    if game is None:
        sys.exit()

    event = pg.event.wait()

    if event.type == pg.QUIT:
        game.stop()
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            game.stop()
            sys.exit()
