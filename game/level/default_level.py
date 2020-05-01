import pygame as pg
from game.model.player import Player
from game.model.layer.map import BackgroundMap


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
                 builded: bool = False):
        self.player: Player = player
        self.bg_map: BackgroundMap = background_map
        self.speed: float = 3.0
        self._run: bool = builded
        self._loaded: bool = False
        if not self._run and (self.player is None or self.bg_map is None):
            self._load()

    def increment_speed(self):
        """
        Increments speed of map
        """
        self.speed += 0.0002

    def get_obstacles(self):
        """
        :return: returns a list of obstacles of bg_map
        """
        return self.bg_map.get_obstacles()

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

    def render(self, tela: pg.Surface):
        """
        Render the objects in this level

        :param tela: pygame Surface screen
        """
        if (not self._run) or (self.player is None or self.bg_map is None):
            return
        self.bg_map.render(tela=tela)
        self.player.render(tela=tela)

        pg.draw.line(tela, (255, 255, 255),
                     self.player.get_sensor().get_center_pos_player(),
                     self.player.get_sensor().get_first_obstacle().to_rect().center)

        pg.draw.line(tela, (255, 255, 255),
                     self.player.get_sensor().get_center_pos_shadow(),
                     self.player.get_sensor().get_first_obstacle().to_rect().center)

    def _load(self,
              player: Player = None,
              background_map: BackgroundMap = None,):
        """
        Loads the default objects of this level if the parameters are none

        :param player: player object
        :param background_map: map object
        """
        self.bg_map = background_map if background_map else BackgroundMap()
        self.player = player if player else Player(background=self.bg_map)

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
