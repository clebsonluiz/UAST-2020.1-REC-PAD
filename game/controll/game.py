import pygame as pg
import game.view.frame as frame
import game.controll.events as e
from game.constants import *

from game.level import DefaultLevel


class Game:

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title='Game Window: PLAYER MODE'):
        self.Frame = frame.Frame(width, height, title)
        self.clock = pg.time.Clock()
        self.FPS: float = 60.0
        self.running = False

        self.font_score = pg.font.SysFont("monospace", 20, bold=True, italic=True)
        self.font_credits = pg.font.SysFont("monospace", 12, bold=True, italic=True)
        self.font_fps = pg.font.SysFont("monospace", 20, bold=True, italic=True)
        self.font_debug = pg.font.SysFont("monospace", 12, bold=True, italic=True)
        self.font_neural = pg.font.SysFont("monospace", 14, bold=True, italic=True)

        self.level = DefaultLevel()
        self._show_credits: bool = False

    def show_credits(self):
        self._show_credits = not self._show_credits

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

        tela.blit(self.font_fps.render('FPS: {:.2f}'.format(self.clock.get_fps()), 1, WHITE), (SCREEN_WIDTH - 150, 6))
        tela.blit(self.font_score.render(' x {} -=> {}'.format(self.level.player.get_score(), self.level.best_score),
                                         1, WHITE), (20, 6))

        self._credits(tela=tela)
        if self._show_credits:
            # surf: pg.Surface = pg.Surface([237, 248]).convert()
            surf: pg.Surface = pg.Surface([398, 248]).convert()
            surf.fill(BACKGROUND_COLOR)
            surf.set_colorkey(BACKGROUND_COLOR)

            self._inputs(tela=surf, scale=0.65)
            tela.blit(surf, (240, 230))

        self.Frame.update()
        pass

    def _update(self):
        self.level.update()
        pass

    def _credits(self, tela: pg.Surface = None):
        if self._show_credits:
            text = self.level.bg_map.get_credits()
            font: pg.font.Font = self.font_credits
            for line in range(len(text)):
                tela.blit(font.render(text[line], 1, WHITE),
                          (10, SCREEN_HEIGHT * 0.60 + 14 * line))

    def _inputs(self, tela: pg.Surface = None, scale: float = 1):
        if self._show_credits:

            pg.draw.rect(tela, RED, self.level.get_desintegrator().to_rect(scale=scale))

            top = self.level.bg_map.get_limit_top().copy()
            top.y = (top.y - 22) * scale
            top.h = 32 * scale
            top.w = top.w * scale

            bottom = self.level.bg_map.get_limit_bottom().copy()
            bottom.y = bottom.y * scale
            bottom.h = 32 * scale
            bottom.w = bottom.w * scale

            pg.draw.rect(tela, WHITE, top)
            pg.draw.rect(tela, WHITE, bottom)

            pg.draw.rect(tela, WHITE, self.level.player.shadow.to_rect(scale=scale), 2)
            pg.draw.rect(tela, WHITE, self.level.player.player.to_rect(scale=scale), 0)

            obs = self.level.get_obstacles()[0]
            rect_obs = obs.to_rect(scale=scale)
            pg.draw.rect(tela, WHITE, rect_obs)
            if obs.coin_still_in_obstacle():
                pg.draw.rect(tela, YELLOW, obs.get_coin().to_rect(scale=scale))

            sensor = self.level.player.get_sensor()
            if get_render_type()['DEBUG']:
                p = self.level.player.player.to_rect(scale=scale).center

                rect = pg.rect.Rect(p[0], p[1], rect_obs.center[0], rect_obs.center[1])

                pg.draw.line(tela, WHITE, p, rect_obs.center, 2)

                tela.blit(self.font_debug.render(
                    '<-{:.0f}->'.format(sensor.get_curr_dist_player_to_obstacle()),
                    1, WHITE), (rect.center[0] / 2, rect.center[1] / 2))
                p = self.level.player.shadow.to_rect(scale=scale).center
                rect = pg.rect.Rect(p[0], p[1], rect_obs.center[0], rect_obs.center[1])
                pg.draw.line(tela, WHITE, p, rect_obs.center, 2)

                tela.blit(self.font_debug.render(
                    '<-{:.0f}->'.format(sensor.get_curr_dist_shadow_to_obstacle()),
                    1, WHITE), (rect.center[0] / 2, rect.center[1] / 2))

                tela.blit(self.font_debug.render(
                    'v ≈ {:.2f} '.format(sensor.get_curr_speed()),
                    1, WHITE), (tela.get_width() - 70, top.bottom + 30))

                tela.blit(self.font_debug.render(
                    '|-{}-|'.format(sensor.get_curr_width_of_obstacle()),
                    1, BLACK), (rect_obs.center[0] - (4 * 6),
                                (rect_obs.bottom - 10) if not obs.get_coin().is_on_top() else (rect_obs.top - 10)))

            tela.blit(self.font_debug.render(
                '-> Dist. da Sombra: <-{:.0f}->'.format(sensor.get_curr_dist_shadow_to_obstacle()),
                1, WHITE), (4, tela.get_height() - 90))
            tela.blit(self.font_debug.render(
                '-> Dist. do Alien: <-{:.0f}->'.format(sensor.get_curr_dist_player_to_obstacle()),
                1, WHITE), (4, tela.get_height() - 70))
            tela.blit(self.font_debug.render(
                '-> Largura do Obstáculo: |-{:.0f}-| '.format(sensor.get_curr_width_of_obstacle()),
                1, WHITE), (4, tela.get_height() - 50))
            tela.blit(self.font_debug.render(
                '-> Velocidade do Mapa: v ≈ {:.2f} '.format(sensor.get_curr_speed()),
                1, WHITE), (4, tela.get_height() - 30))
