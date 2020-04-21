from typing import List
import pygame as pg
from game.constants import *
from game.model.layer.builder.tile_layer import TileLayer


class BackgroundLayers:
    """
    BackgroundLayers Class
    __________
    Used to build and manage the layers on pygame surface
    """

    def __init__(self):
        self._rect_top = pg.rect.Rect(0, (SCREEN_HEIGHT * 0.3) - 10, SCREEN_WIDTH, 10)
        self._rect_bottom = pg.rect.Rect(0, SCREEN_HEIGHT * 0.6, SCREEN_WIDTH, 10)

        self._bg: TileLayer = TileLayer(MATRIX_BACKGROUND_LAYER, vec_x=-0.5)
        self._bg.set_position((0, self._rect_top.bottom))
        self._layer_1: TileLayer = TileLayer(MATRIX_LAYER_1, vec_x=-1.0)
        self._layer_1.set_position((0, self._rect_bottom.top))
        self._layer_2: TileLayer = TileLayer(MATRIX_LAYER_1, vec_x=-1.0, invert_y=True)
        self._layer_2.set_position((0, self._rect_top.bottom -
                                    self._layer_2.get_layer().
                                    get_image().get_height()))

    def get_intern_rect(self) -> pg.Rect:
        """
        Gets the pygame.Rect of intern background of between
        collison top and collision botton rects as positioned
        :return: pygame.Rect of background
        """
        x: float = 0.0
        y: float = self.get_limit_top().bottom
        width: float = SCREEN_WIDTH
        height: float = self.get_limit_bottom().top - self.get_limit_top().bottom
        return pg.Rect(x, y, width, height)

    def get_limit_top(self) -> pg.Rect:
        """
        :return: pygame.Rect of the limit top of the map
        """
        return self._rect_top

    def get_limit_bottom(self) -> pg.Rect:
        """
        :return: pygame.Rect of the limit bottom of the map
        """
        return self._rect_bottom

    def get_background_layer(self) -> TileLayer:
        """
        :return: TileLayer used to be the firt layer (Background)
        """
        return self._bg

    def get_top_layer(self) -> TileLayer:
        """
        :return: TileLayer used to be the second layer (top layer)
        """
        return self._layer_1

    def get_bottom_layer(self) -> TileLayer:
        """
        :return: TileLayer used to be the third layer (bottom layer)
        """
        return self._layer_2

    def update(self, speed: float = 1.0):
        """
        Updates the layers with the same speed
        """
        self._bg.update(speed=speed)
        self._layer_1.update(speed=speed)
        self._layer_2.update(speed=speed)

    def render(self, tela: pg.Surface):
        """
        Render the layers on Surface

        :param tela: pygame Surface when the layers are drawed in
        """
        if tela is None:
            return
        self._bg.render(tela=tela, loop=True)
        self._layer_1.render(tela=tela, loop=True)
        self._layer_2.render(tela=tela, loop=True)
