import pygame as pg
import game.view.frame as frame
import game.controll.events as e
from game.constants import *

from game.model.layer import BackgroundMap
from game.model.player import Player
from game.level import DefaultLevel


class Game:

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title='Game Window'):
        self.Frame = frame.Frame(width, height, title)
        self.clock = pg.time.Clock()
        self.FPS: float = 60.0
        self.running = False

        # self.map = BackgroundMap()
        # self.player = Player(self.map)
        # self.map_speed = 3.0
        self.font_score = pg.font.SysFont("monospace", 20)
        self.font_credits = pg.font.SysFont("monospace", 12, italic=True)
        self.font_fps = pg.font.SysFont("monospace", 20, italic=True)

        self.level = DefaultLevel()

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
        if tela is None or not self.level.loaded() or not self.level.is_ready():
            return
        tela.fill(BACKGROUND_COLOR)

        self.level.render(tela=tela)

        # self.map.render(tela=tela)
        # self.player.render(tela=tela)

        tela.blit(self.font_fps.render('FPS: {:.2f}'.format(self.clock.get_fps()), 1, WHITE), (SCREEN_WIDTH - 150, 10))
        tela.blit(self.font_score.render(' x ' + str(self.level.player.get_score()), 1, WHITE), (20, 10))
        self._credits(tela=tela)
        tela.blit(self.font_fps.render('Speed: {:.3f}'.format(self.level.speed), 1, WHITE),
                  (SCREEN_WIDTH - 150, 30))

        # pg.draw.rect(tela, WHITE, pg.Rect(240, 270, 398, 208), 1)
        # pg.draw.line(tela, WHITE, (240, 270), (638, 478))
        #
        # pg.draw.circle(tela, WHITE, (260, 290), 15, 1)
        # pg.draw.circle(tela, WHITE, (260, 340), 15, 1)
        # pg.draw.circle(tela, WHITE, (260, 400), 15, 1)
        # pg.draw.circle(tela, WHITE, (260, 450), 15, 1)
        #
        # pg.draw.circle(tela, WHITE, (380, 340), 25, 1)
        # pg.draw.circle(tela, WHITE, (380, 400), 25, 1)
        #
        # pg.draw.circle(tela, WHITE, (530, 340), 20, 1)
        # pg.draw.circle(tela, WHITE, (530, 400), 20, 1)

        # obs = self.map.get_obstacles()[0]
        # if obs.to_rect().colliderect(self.player.to_rect()):
        #     tela.blit(self.font_fps.render('COLIDINDO', 1, WHITE),
        #               (SCREEN_WIDTH - 140, 30))
        self.Frame.update()
        pass

    def _update(self):
        # self.map.update(speed=self.map_speed)
        # self.player.update()
        self.level.update()
        pass

    def _credits(self, tela: pg.Surface = None):
        text = self.level.bg_map.get_credits()
        font: pg.font.Font = self.font_credits
        for line in range(len(text)):
            tela.blit(font.render(text[line], 1, WHITE),
                      (10, SCREEN_HEIGHT * 0.70 + 14 * line))
