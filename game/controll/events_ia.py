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
            elif event.key == pg.K_DOWN:
                game.ia_level.get_O_MELHOR_JOGADOR().save_in_file()
            # elif event.key == pg.K_RIGHT:
            #     game.level.player.do_jump()
            # elif event.key == pg.K_UP:
            #     game.level.player.do_change_gravit()
            # elif event.key == pg.K_SPACE:
            #     game.level.reload()
    if game.ia_level.loaded() and game.ia_level.is_ready():
        check_coin_colision(game=game)
        check_dificult(game=game)


def check_coin_colision(game):
    obs = game.ia_level.get_obstacles()[0]
    desintegrator = game.ia_level.get_desintegrator()

    if desintegrator.to_rect().colliderect(game.ia_level.get_O_ATUAL_JOGADOR().to_rect()):
        game.level.stop()
        game.ia_level.restart()
    if obs.to_rect().colliderect(game.ia_level.get_O_ATUAL_JOGADOR().to_rect()):
        # game.stop()
        game.ia_level.stop()
        game.ia_level.restart()
    if obs.is_out_screen() and obs.coin_still_in_obstacle():
        game.ia_level.get_O_ATUAL_JOGADOR().decrement_score()
        game.ia_level.increment_x_of_desintegrator_in()
    if game.ia_level.get_O_ATUAL_JOGADOR().to_rect().colliderect(obs.get_coin().to_rect()) and obs.coin_still_in_obstacle():
        obs.make_coin_colision()
        game.ia_level.get_O_ATUAL_JOGADOR().increment_score()


def check_dificult(game):

    if game.ia_level.get_O_ATUAL_JOGADOR().get_score() < 20:
        if game.ia_level.speed < 3.3:
            game.ia_level.increment_speed()
    if 20 <= game.ia_level.get_O_ATUAL_JOGADOR().get_score() < 50:
        game.ia_level.IA.BG_MAP.ObstacleBuilder.set_dificult_type('normal')
        if game.ia_level.speed < 4.0:
            game.ia_level.speed = 4.0
        if game.ia_level.speed < 5.0:
            game.ia_level.increment_speed()
    elif game.ia_level.get_O_ATUAL_JOGADOR().get_score() >= 50:
        game.ia_level.IA.BG_MAP.ObstacleBuilder.set_dificult_type('hard')
        if game.ia_level.speed < 6.0:
            game.ia_level.increment_speed()