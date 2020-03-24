__author__ = 'Clébson Luiz'
__version__ = "0.1"
__description__ = "Projeto de disciplina para a cadeira Reconhecimento de Padrões 2020.1"
__credits__ = 'Todos os sprites ou imagens usadas são de creditos dos seus criadores/decoders'

import pygame as pg

from game.controll.game import Game


pg.init()

try:
    game = Game()
    game.start()
except Exception as ex:
    print(ex)

finally:
    pg.quit()
