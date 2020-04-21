from typing import List
import pygame as pg
from game.model.layer.obstacle import Obstacle
from .obstacle import ObstacleConstruct
from .background import BackgroundLayers


class BackgroundMap:
    """
    BackgroundMap Class
    __________
    Used to be a facility class to make the
    conjunct of the layers and obstacles more acessible in main Game class
    """

    def __init__(self):
        self.BgLayers = BackgroundLayers()
        self.ObstacleBuilder = ObstacleConstruct(background_layers=self.BgLayers)
        self.ObstacleBuilder.generate(self.BgLayers, firsts=True)

    def get_background_rect(self) -> pg.Rect:
        """
        Gets the pygame.Rect of intern background of between
        collison top and collision botton rects as positioned
        :return: pygame.Rect of background
        """
        return self.BgLayers.get_intern_rect()

    def get_limit_top(self) -> pg.Rect:
        """
        :return: pygame.Rect of the limit top of the map
        """
        return self.BgLayers.get_limit_top()

    def get_limit_bottom(self) -> pg.Rect:
        """
        :return: pygame.Rect of the limit bottom of the map
        """
        return self.BgLayers.get_limit_bottom()

    def get_obstacles(self) -> List[Obstacle]:
        """
        :return: List of obstacles
        """
        return self.ObstacleBuilder.get_obstacles()

    def update(self, speed: float = 1.0):
        """
        Updates the layers and obstacles with the same speed
        """
        self.BgLayers.update(speed=speed)
        self.ObstacleBuilder.update(speed=speed)

    def render(self, tela: pg.Surface):
        """
        Render the layers and obstacles on Surface

        :param tela: pygame Surface when the layers and obstacles are drawed in
        """
        self.BgLayers.render(tela=tela)
        self.ObstacleBuilder.render(tela=tela)
