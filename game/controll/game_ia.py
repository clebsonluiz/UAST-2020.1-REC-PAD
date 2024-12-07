import pygame as pg
import game.view.frame as frame
import game.controll.events_ia as e
from game.constants import *
from game.level.default_level_ia import DefaultLevelIA
import sys as system


class GameIA:

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title='Game Window: IA MODE'):
        self.Frame = frame.Frame(width, height, title)
        self.clock = pg.time.Clock()
        self.FPS: float = 60.0
        self.running = False

        self.font_score = pg.font.SysFont("monospace", 20, bold=True, italic=True)
        self.font_credits = pg.font.SysFont("monospace", 12, bold=True, italic=True)
        self.font_fps = pg.font.SysFont("monospace", 18, bold=True, italic=True)
        self.font_debug = pg.font.SysFont("monospace", 12, bold=True, italic=True)
        self.ia_level = DefaultLevelIA()
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
        if tela is None or not self.ia_level.loaded() or not self.ia_level.is_ready():
            return
        tela.fill(BACKGROUND_COLOR)

        self.ia_level.render(tela=tela)

        tela.blit(self.font_fps.render('FPS: {:.2f}'.format(self.clock.get_fps()), 1, WHITE), (SCREEN_WIDTH - 150, 6))
        tela.blit(self.font_score.render(' x {} -=> {}'.format(
            self.ia_level.get_O_ATUAL_JOGADOR().get_score(),
            self.ia_level.get_O_MELHOR_JOGADOR().get_score()), 1, WHITE), (20, 6))

        self._credits(tela=tela)
        if not self._show_credits:
            surf: pg.Surface = pg.Surface([237, 248]).convert()
            surf.fill(BACKGROUND_COLOR)
            surf.set_colorkey(BACKGROUND_COLOR)

            self._inputs(tela=surf, scale=0.5)
            tela.blit(surf, (2, 230))
        self._neural(tela=tela)
        pg.draw.rect(tela, WHITE, pg.Rect(240, 230, 398, 248), 1)

        self.Frame.update()
        pass

    def _update(self):
        self.ia_level.update()
        pass

    def _credits(self, tela: pg.Surface = None):
        if self._show_credits:
            text = self.ia_level.IA.BG_MAP.get_credits()
            font: pg.font.Font = self.font_credits
            for line in range(len(text)):
                tela.blit(font.render(text[line], 1, WHITE),
                          (10, SCREEN_HEIGHT * 0.60 + 14 * line))
        pg.draw.rect(tela, WHITE, pg.Rect(2, 230, 237, 248), 1)

    def _inputs(self, tela: pg.Surface = None, scale: float = 1):
        if not self._show_credits:

            pg.draw.rect(tela, RED, self.ia_level.get_desintegrator().to_rect(scale=scale))

            top = self.ia_level.IA.BG_MAP.get_limit_top().copy()
            top.y = int((top.y - 22) * scale)
            top.h = int(32 * scale)
            top.w = int(top.w * scale)

            bottom = self.ia_level.IA.BG_MAP.get_limit_bottom().copy()
            bottom.y = int(bottom.y * scale)
            bottom.h = int(32 * scale)
            bottom.w = int(bottom.w * scale)

            pg.draw.rect(tela, WHITE, top)
            pg.draw.rect(tela, WHITE, bottom)

            pg.draw.rect(tela, WHITE, self.ia_level.get_O_ATUAL_JOGADOR().shadow.to_rect(scale=scale), 2)
            pg.draw.rect(tela, WHITE, self.ia_level.get_O_ATUAL_JOGADOR().player.to_rect(scale=scale), 0)

            obs = self.ia_level.get_obstacles()[0]
            rect_obs = obs.to_rect(scale=scale)
            pg.draw.rect(tela, WHITE, rect_obs)
            if obs.coin_still_in_obstacle():
                pg.draw.rect(tela, YELLOW, obs.get_coin().to_rect(scale=scale))

            sensor = self.ia_level.get_O_ATUAL_JOGADOR().get_sensor()
            if get_render_type()['DEBUG']:
                p = self.ia_level.get_O_ATUAL_JOGADOR().player.to_rect(scale=scale).center

                rect = pg.rect.Rect(p[0], p[1], rect_obs.center[0], rect_obs.center[1])

                pg.draw.line(tela, WHITE, p, rect_obs.center, 2)

                tela.blit(self.font_debug.render(
                    '<-{:.0f}->'.format(sensor.get_curr_dist_player_to_obstacle()),
                    1, WHITE), (rect.center[0] / 2, rect.center[1] / 2))

                p = self.ia_level.get_O_ATUAL_JOGADOR().shadow.to_rect(scale=scale).center
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

            pg.draw.rect(tela, WHITE, pg.Rect(0, 0, 237, 248), 1)

    def _neural(self, tela: pg.Surface = None):
        vec = [
            (290, 260),
            (290, 310),
            (290, 370),
            (290, 420),

            (400, 280),
            (400, 400),

            (470, 310),
            (470, 370),

            (510, 310),
            (510, 370),
        ]

        R = self.ia_level.get_O_ATUAL_JOGADOR().cerebro.get_input_renders()

        pg.draw.line(tela, RED if R[1][0] else WHITE, vec[0], vec[4], 3 if R[1][0] else 1)
        pg.draw.line(tela, RED if R[1][0] else WHITE, vec[1], vec[4], 3 if R[1][0] else 1)
        pg.draw.line(tela, RED if R[1][0] else WHITE, vec[2], vec[4], 3 if R[1][0] else 1)
        pg.draw.line(tela, RED if R[1][0] else WHITE, vec[3], vec[4], 3 if R[1][0] else 1)

        pg.draw.line(tela, RED if R[1][1] else WHITE, vec[0], vec[5], 3 if R[1][1] else 1)
        pg.draw.line(tela, RED if R[1][1] else WHITE, vec[1], vec[5], 3 if R[1][1] else 1)
        pg.draw.line(tela, RED if R[1][1] else WHITE, vec[2], vec[5], 3 if R[1][1] else 1)
        pg.draw.line(tela, RED if R[1][1] else WHITE, vec[3], vec[5], 3 if R[1][1] else 1)

        pg.draw.line(tela, RED if R[2][0] and R[1][0] else WHITE, vec[4], vec[6], 3 if R[2][0] else 1)
        pg.draw.line(tela, RED if R[2][1] and R[1][1] else WHITE, vec[4], vec[7], 3 if R[2][1] else 1)

        pg.draw.line(tela, RED if R[2][0] and R[1][0] else WHITE, vec[5], vec[6], 3 if R[2][0] else 1)
        pg.draw.line(tela, RED if R[2][1] and R[1][1] else WHITE, vec[5], vec[7], 3 if R[2][1] else 1)

        pg.draw.line(tela, RED if R[2][0] else WHITE, vec[6], vec[8], 3 if R[2][0] else 1)
        pg.draw.line(tela, RED if R[2][1] else WHITE, vec[7], vec[9], 3 if R[2][1] else 1)

        pg.draw.circle(tela, RED if R[0][0] else WHITE, vec[0], 10)
        pg.draw.circle(tela, RED if R[0][1] else WHITE, vec[1], 10)
        pg.draw.circle(tela, RED if R[0][2] else WHITE, vec[2], 10)
        pg.draw.circle(tela, RED if R[0][3] else WHITE, vec[3], 10)
        #
        pg.draw.circle(tela, RED if R[1][0] else WHITE, vec[4], 20)
        pg.draw.circle(tela, RED if R[1][1] else WHITE, vec[5], 20)
        #
        pg.draw.circle(tela, RED if R[2][0] else WHITE, vec[6], 15)
        pg.draw.circle(tela, RED if R[2][1] else WHITE, vec[7], 15)

        tela.blit(self.font_fps.render('PULAR', 1, WHITE), (vec[8][0], vec[8][1] - 10))
        tela.blit(self.font_fps.render('INVERTER', 1, WHITE), (vec[9][0], vec[9][1] - 10))

        tela.blit(self.font_debug.render('REPRESENTAÇÃO ABSTRATA DA REDE NEURAL', 1, WHITE),
                  (300, 240))

        tela.blit(self.font_fps.render('GERAÇÃO Nº: {} | INDIVIDUO Nº: {}'.format(
            self.ia_level.get_O_ATUAL_JOGADOR().geracao,
            self.ia_level.get_O_ATUAL_JOGADOR().numero,
        ), 1, WHITE), (250, 440))
