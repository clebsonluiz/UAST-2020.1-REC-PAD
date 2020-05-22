import pygame as pg
import sys


def events(game):
    if game is None:
        sys.exit()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game.stop()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                game.stop()
                sys.exit()
            elif event.key == pg.K_RIGHT:
                game.level.player.do_jump()
            elif event.key == pg.K_UP:
                game.level.player.do_change_gravit()
            elif event.key == pg.K_SPACE:
                game.level.reload()
            elif event.key == pg.K_DOWN:
                game.show_credits()

    check_coin_colision(game=game)
    check_dificult(game=game)


def check_coin_colision(game):
    obs = game.level.bg_map.get_obstacles()[0]
    desintegrator = game.level.get_desintegrator()
    if desintegrator.to_rect().colliderect(game.level.player.to_rect()):
        game.level.stop()
    if obs.to_rect().colliderect(game.level.player.to_rect()):
        game.level.stop()
    if obs.is_out_screen() and obs.coin_still_in_obstacle():
        game.level.player.decrement_score()
        game.level.increment_x_of_desintegrator_in()
    if game.level.player.to_rect().colliderect(obs.get_coin().to_rect()) and obs.coin_still_in_obstacle():
        obs.make_coin_colision()
        game.level.player.increment_score()
        game.level.update_best_score()


def check_dificult(game):

    if game.level.player.get_score() < 20:
        if game.level.speed < 3.9:
            game.level.increment_speed()
    if 20 <= game.level.player.get_score() < 50:
        game.level.bg_map.ObstacleBuilder.set_dificult_type('normal')
        if game.level.speed < 4.0:
            game.level.speed = 4.0
        if game.level.speed < 5.0:
            game.level.increment_speed()
    elif 50 <= game.level.player.get_score() < 100:
        game.level.bg_map.ObstacleBuilder.set_dificult_type('hard')
        if game.level.speed < 8.0:
            game.level.increment_speed()
    elif game.level.player.get_score() > 100:
        game.level.bg_map.ObstacleBuilder.set_dificult_type('hard')
        game.level.increment_speed()
