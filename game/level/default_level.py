import pygame as pg
from game.model.player import Player
from game.model.layer.map import BackgroundMap
from game.model.desintegrator import Desintegrator


class DefaultLevel:
    """
    Default Level Class who represents the level will be used to be played

    Parameters
    __________
    player: Player
        Player of the will be integrate to this level
    background: BackgroundMap
        Colision layer of the player object to this level
    builded: bool
        Bool value that represents if the class as a parameters and is ready to run
    """
    def __init__(self,
                 player: Player = None,
                 background_map: BackgroundMap = None,
                 desintegrator: Desintegrator = None,
                 builded: bool = False):
        self.player: Player = player
        self.bg_map: BackgroundMap = background_map
        self.speed: float = 3.0
        self._run: bool = builded
        self._loaded: bool = False
        self._desintegrator = desintegrator
        self.best_score: int = 0
        if not self._run and (self.player is None or self.bg_map is None):
            self._load()

    def update_best_score(self):
        if self.best_score < self.player.get_score():
            self.best_score = self.player.get_score()

    def increment_speed(self):
        """
        Increments speed of map
        """
        self.speed += 0.0004

    def increment_x_of_desintegrator_in(self, more: int = 15):
        """
        :param more: value will be incremented in x axis of desintegrator
        """
        if self._desintegrator:
            self._desintegrator.increment_maximum_x_in(more=more)

    def get_obstacles(self):
        """
        :return: returns a list of obstacles of bg_map
        """
        return self.bg_map.get_obstacles()

    def get_desintegrator(self):
        return self._desintegrator

    def loaded(self):
        """
        :return: True if the sprites is loaded
        """
        if self.player is None or self.bg_map is None:
            return False
        return self.player.loaded()

    def is_ready(self) -> bool:
        """
        :return: True if is ready to be used
        """
        return self._run

    def update(self):
        """
        Updates the state of this level
        """
        if (not self._run) or (self.player is None or self.bg_map is None):
            return
        self.bg_map.update(speed=self.speed)
        self.player.update()
        self._desintegrator.update()

    def render(self, tela: pg.Surface):
        """
        Render the objects in this level

        :param tela: pygame Surface screen
        """
        if (not self._run) or (self.player is None or self.bg_map is None):
            return
        self.bg_map.render(tela=tela)
        self.player.render(tela=tela)
        self._desintegrator.render(tela=tela)

        # pg.draw.line(tela, (255, 255, 255),
        #              self.player.get_sensor().get_center_pos_player(),
        #              self.player.get_sensor().get_first_obstacle().to_rect().center)
        #
        # pg.draw.line(tela, (255, 255, 255),
        #              self.player.get_sensor().get_center_pos_shadow(),
        #              self.player.get_sensor().get_first_obstacle().to_rect().center)

    def _load(self,
              player: Player = None,
              background_map: BackgroundMap = None,):
        """
        Loads the default objects of this level if the parameters are none

        :param player: player object
        :param background_map: map object
        """
        if background_map or self.bg_map is None:
            self.bg_map = background_map if background_map else BackgroundMap()
        else:
            self.bg_map.ObstacleBuilder.reset()
        self.player = player if player else Player(background=self.bg_map)
        self._desintegrator = Desintegrator(background=self.bg_map)
        self._desintegrator.increment_maximum_x_in(30)
        self.speed = 3.0
        self._run = True

    def reload(self,
               player: Player = None,
               background_map: BackgroundMap = None):
        """
        Reloads this object level and objects map to the default or from parameters

        :param player: player object
        :param background_map: map object
        """
        self.stop()
        self._load(background_map=background_map, player=player)

    def stop(self):
        """
        Stops the level and make this to not ready
        """
        self._run = False
