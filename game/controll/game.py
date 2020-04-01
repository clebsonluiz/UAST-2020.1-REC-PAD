import pygame as pg
import game.view.frame as frame
import game.controll.events as e
from game.constants import *
import os

from game.model.map import BackgroundMap
from game.model.player import Player

class Game:

    def __init__(self, width=640, height=480, title='Game Window'):
        self.Frame = frame.Frame(width, height, title)
        self.clock = pg.time.Clock()
        self.FPS: float = 30.0
        self.running = False

        self.map = BackgroundMap()
        self.player = Player(self.map)
        self.player.make_animations_list()
        self.player.pos_x = 20
        self.player.pos_y = 200
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
        tela.fill(WHITE, self.map.get_limit_top())
        tela.fill(WHITE, self.map.get_limit_bottom())
        tela.blit(self.player.current_sprite(), self.player.get_position())
        tela.blit(pg.font.SysFont("monospace", 20).render('Score: ' + str(0), 1, WHITE), (10, 10))
        self.Frame.update()

        pass

    def _update(self,):
        self.player.update()
        pass
