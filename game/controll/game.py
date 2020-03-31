import pygame as pg
import game.view.frame as frame
import game.controll.events as e
from game.constants import *
import os

from game.model.player import Player

class Game:

    def __init__(self, width=640, height=480, title='Game Window'):
        self.Frame = frame.Frame(width, height, title)
        self.clock = pg.time.Clock()
        self.FPS: float = 30.0
        self.running = False

        self.player = Player()
        self.player.make_animations_list()
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
            self.clock.tick(self.FPS)
            pass
        pass

    def _render(self, tela: pg.Surface = None):
        if tela is None or not self.player.loaded():
            return
        tela.fill(BLACK)
        tela.blit(self.player.current_sprite(), (280, 190))

        self.Frame.update()

        pass

    def _update(self,):
        self.player.update()
        pass
