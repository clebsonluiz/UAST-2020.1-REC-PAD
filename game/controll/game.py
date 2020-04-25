import pygame as pg
import game.view.frame as frame
import game.controll.events as e
from game.constants import *

from game.model.layer import BackgroundMap
from game.model.player import Player


class Game:

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title='Game Window'):
        self.Frame = frame.Frame(width, height, title)
        self.clock = pg.time.Clock()
        self.FPS: float = 60.0
        self.running = False

        self.map = BackgroundMap()
        self.player = Player(self.map)
        self.map_speed = 3.0
        self.font_score = pg.font.SysFont("monospace", 20)
        self.font_credits = pg.font.SysFont("monospace", 12, italic=True)
        self.font_fps = pg.font.SysFont("monospace", 20, italic=True)

    def increment_speed(self):
        self.map_speed += 0.0002

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
        tela.fill(BACKGROUND_COLOR)
        self.map.render(tela=tela)
        self.player.render(tela=tela)
        tela.blit(self.font_fps.render('FPS: {:.2f}'.format(self.clock.get_fps()), 1, WHITE), (SCREEN_WIDTH - 140, 10))
        tela.blit(self.font_score.render(' x ' + str(self.player.get_score()), 1, WHITE), (20, 10))
        self._credits(tela=tela)
        tela.blit(self.font_fps.render('Speed: {:.3f}'.format(self.map_speed), 1, WHITE),
                  (SCREEN_WIDTH - 140, 30))
        # obs = self.map.get_obstacles()[0]
        # if obs.to_rect().colliderect(self.player.to_rect()):
        #     tela.blit(self.font_fps.render('COLIDINDO', 1, WHITE),
        #               (SCREEN_WIDTH - 140, 30))
        self.Frame.update()
        pass

    def _update(self):
        self.map.update(speed=self.map_speed)
        self.player.update()
        pass

    def _credits(self, tela: pg.Surface = None):
        text = self.map.get_credits()
        font: pg.font.Font = self.font_credits
        for line in range(len(text)):
            tela.blit(font.render(text[line], 1, WHITE),
                      (10, SCREEN_HEIGHT * 0.70 + 14 * line))
