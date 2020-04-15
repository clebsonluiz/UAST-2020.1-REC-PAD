import pygame as pg
import sys


def events(game):
    if game is None:
        sys.exit()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game.stop()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                game.stop()
                sys.exit()
            elif event.key == pg.K_RIGHT:
                game.player.do_jump()
            elif event.key == pg.K_UP:
                game.player.do_change_gravit()
    # event = pg.event.wait()
    #
    # if event.type == pg.QUIT:
    #     game.stop()
    # elif event.type == pg.KEYDOWN:
    #     if event.key == pg.K_ESCAPE:
    #         game.stop()
    #         sys.exit()
