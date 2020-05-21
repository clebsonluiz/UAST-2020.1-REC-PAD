__author__ = 'Clébson Luiz'
__version__ = "0.1"
__description__ = "Projeto de disciplina para a cadeira Reconhecimento de Padrões 2020.1"
__credits__ = 'Todos os sprites ou imagens usadas são de creditos dos seus criadores/decoders'

import pygame as pg

from game.controll.game import Game
from game.constants import set_render_type

from game.controll.game_ia import GameIA
from game.model.file import close_all


GAME_AI_MODE = False

pg.init()

try:
    set_render_type({'NORMAL': False, 'COLISION': True, 'DEBUG': True})
    if GAME_AI_MODE:
        game = GameIA()
    else:
        game = Game()
    game.start()
except Exception as ex:
    print(ex)

finally:
    pg.quit()
    close_all()
