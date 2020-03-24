import pygame as pg
import game.view.frame as frame
import game.controll.events as e
from game.constants import *
import os

class Game:

    def __init__(self, width=640, height=480, title='Game Window'):
        self.Frame = frame.Frame(width, height, title)
        self.clock = pg.time.Clock()
        self.running = False

        self.logo = pg.image.load(SPRITE_SHEET_NAME)

        pass

    def start(self):
        self.running = True
        print('Status Game Runnig: ', self.running)
        self.loop()
        pass

    def stop(self):
        self.running = False
        print('Status Game Runnig: ', self.running)
        print('Games as Stoped')

    def loop(self):
        while self.running:
            e.events(self)
            self._update()
            self._render(self.Frame.get_tela())
            pass
        pass

    def _render(self, tela: pg.Surface = None):
        if tela is None:
            return
        tela.fill([30, 30, 30])
        tela.blit(self.logo, [280, 190])

        self.Frame.update()

        pass

    def _update(self, gt=None):
        pass
