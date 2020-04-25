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

    check_coin_colision(game=game)
    check_dificult(game=game)


def check_coin_colision(game):
    obs = game.map.get_obstacles()[0]
    if obs.to_rect().colliderect(game.player.to_rect()):
        game.stop()
        sys.exit()
    if obs.is_out_screen() and obs.coin_still_in_obstacle():
        game.player.decrement_score()
    if game.player.to_rect().colliderect(obs.get_coin().to_rect()) and obs.coin_still_in_obstacle():
        obs.make_coin_colision()
        game.player.increment_score()


def check_dificult(game):

    if game.player.get_score() < 20:
        if game.map_speed < 3.3:
            game.increment_speed()
    if 20 <= game.player.get_score() < 50:
        game.map.ObstacleBuilder.set_dificult_type('normal')
        if game.map_speed < 4.0:
            game.increment_speed()
    elif game.player.get_score() >= 50:
        game.map.ObstacleBuilder.set_dificult_type('hard')
        if game.map_speed < 6.0:
            game.increment_speed()
