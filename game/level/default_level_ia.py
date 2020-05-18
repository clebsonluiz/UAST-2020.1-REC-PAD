import pygame as pg
# from game.model.player import Player
from game.model.desintegrator import Desintegrator
from game.ia import SelecaoNatural


class DefaultLevelIA:
    """
    Default Level IA Class who represents the level will be used to traning a IA
    """

    def __init__(self):
        self.IA = SelecaoNatural(qtd_individuos=50)
        self.speed: float = 3.0
        self._run: bool = False
        self._loaded: bool = False
        self._desintegrator = None
        if not self._run:
            self.start()

    def increment_x_of_desintegrator_in(self, more: int = 15):
        """
        :param more: value will be incremented in x axis of desintegrator
        """
        if self._desintegrator:
            self._desintegrator.increment_maximum_x_in(more=more)

    def increment_speed(self):
        """
        Increments speed of map
        """
        self.speed += 0.0002

    def get_obstacles(self):
        """
        :return: returns a list of obstacles of BG_MAP
        """
        return self.IA.BG_MAP.get_obstacles()

    def get_desintegrator(self):
        """
        :return: the desintegrator
        """
        return self._desintegrator

    def get_O_MELHOR_JOGADOR(self):
        """
        :return: returns the Current best Player of IA Generation
        """
        return self.IA.O_MELHOR

    def get_O_ATUAL_JOGADOR(self):
        """
        :return: returns the Current Player of IA Generation
        """
        return self.IA.O_ATUAL

    def loaded(self):
        """
        :return: True if the sprites is loaded
        """
        return self.IA.is_loaded()

    def is_ready(self) -> bool:
        """
        :return: True if is ready to be used
        """
        return self._run

    def update(self):
        """
        Updates the state of this level
        """
        if (not self._run) or (not self.IA.is_loaded()):
            return
        self.IA.BG_MAP.update(speed=self.speed)
        self.IA.O_ATUAL.update()
        self._desintegrator.update()

    def render(self, tela: pg.Surface):
        """
        Render the objects in this level

        :param tela: pygame Surface screen
        """
        if (not self._run) or (not self.IA.is_loaded()):
            return
        self.IA.BG_MAP.render(tela=tela)
        self.IA.O_ATUAL.render(tela=tela)
        self._desintegrator.render(tela=tela)

        # pg.draw.line(tela, (255, 255, 255),
        #              self.player.get_sensor().get_center_pos_player(),
        #              self.player.get_sensor().get_first_obstacle().to_rect().center)
        #
        # pg.draw.line(tela, (255, 255, 255),
        #              self.player.get_sensor().get_center_pos_shadow(),
        #              self.player.get_sensor().get_first_obstacle().to_rect().center)

    def start(self):
        """
        Loads the default objects of this level if the parameters are none

        """
        self.IA.start()
        self._desintegrator = Desintegrator(background=self.IA.BG_MAP)
        self._desintegrator.increment_maximum_x_in(30)
        self.speed = 3.0
        self._run = True

    def restart(self):
        """
        Reloads this object level and objects map to the default or from parameters

        """
        self.stop()
        self.IA.restart()
        self._desintegrator = Desintegrator(background=self.IA.BG_MAP)
        self._desintegrator.increment_maximum_x_in(30)
        self.speed = 3.0
        self._run = True

    def stop(self):
        """
        Stops the level and make this to not ready
        """
        self._run = False
        self.IA.stop()
