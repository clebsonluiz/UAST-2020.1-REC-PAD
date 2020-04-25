from typing import List
# from random import randint as next_int
import pygame as pg

from ..builder import TileLayer

from ..background import BackgroundLayers
from ...score.coin import Coin


class Obstacle(TileLayer):
    """
    Class Obstacle(TileLayer) for build the obstacle
    that will render on map background

    Parameters
    __________
        tile_map : List[List[float]]
            Matrix of float tiles
        background_layers : BackgroundLayers
            BackgroundLayers class to used to set the positions of obscales on her
        x : float
            x position on map
        y : float
            y position on map
        dx : float
            x direction when layer is moved
        dy : float
            y direction when layer is moved
    """

    def __init__(self, tile_map: List[List[float]], background_layers: BackgroundLayers,
                 x=0.0, y=0.0, dx=0.0, dy=0.0, ):
        super().__init__(tile_map, vec_x=dx, vec_y=dy)
        self.set_position((x, y))
        self._curr_width = self.get_layer().get_image().get_width()
        self._curr_width = self.get_layer().get_image().get_width()
        self._padding: pg.Rect = pg.Rect(0, 0, 0, 0)
        self._bg_layers: BackgroundLayers = background_layers
        self._coin = None
        self._coin_colision: bool = False

    def get_coin(self) -> Coin:
        return self._coin

    def coin_still_in_obstacle(self):
        return not self._coin_colision

    def make_coin_colision(self):
        self._coin_colision = True

    def build_coin(self, position_up: bool):
        self._coin = Coin(is_on_top=position_up)
        self._coin.set_position_on_rect_obstacle(self)
        self._coin.set_dx(self.get_dx())

    def set_colision_padding(self, padding: pg.Rect = pg.Rect(0, 0, 0, 0)):
        """
        :param padding: pygame Rect used to set padding size of the colision box from object
        """
        self._padding = padding

    # def resets_size(self):
    #     self._curr_width = self.get_layer().get_image().get_width()
    #     self._curr_width = self.get_layer().get_image().get_width()

    def set_vector(self, dx: float = 0.0, dy: float = 0.0):
        """
        sets the vector of the obstacle

        :param dx: x direction when the obstacle is moved
        :param dy: y direction when the obstacle is moved
        """
        self._vec_x = dx
        self._vec_y = dy

    def get_last_distance(self, default: int = 100) -> int:
        """
        Generates the distance between the obstacles
        :param default: default distance
        :return: the distance in int value
        """
        return int(self.get_position()[0] + self._curr_width * 2) + default

    def to_rect(self, x: float = None, y: float = None) -> pg.Rect:
        """
        Generates a colison pygame rect of the obstacle with the padding applied

        :return: a pygame Rect with xy positions and size
        """
        if self._padding is None:
            self._padding = pg.rect.Rect(0, 0, 0, 0)
        return pg.rect.Rect(
            self.pos_x - self._padding.left,
            self.pos_y - self._padding.top,
            self.get_layer().get_image().get_width() - self._padding.right,
            self.get_layer().get_image().get_height() - self._padding.bottom)

    def is_out_screen(self) -> bool:
        """
        :return: if the first obstacle is not more visible in screen
        """
        return (self.get_position()[0] + self.get_layer().get_image().get_width()) <= 0.0

    def update(self, speed: float = 1):
        """
        :param speed: speed movement of obstacle
        """
        self.pos_x += self._vec_x * speed
        self.pos_y += self._vec_y * speed
        if not self._coin_colision:
            self._coin.set_dx(self.get_dx() * speed)
            self._coin.update()

        if self.pos_x <= 0.0:
            pass
        # else:
        #     self._curr_width -= abs(int(self._vec_x * speed))

    def my_relative_positon_on_map(self, position_up: bool = False) -> int:
        """
        Generates the position of obstacle, if he will be on top or bottom
        :param position_up: if he is in top
        :return: the y position when the obstacle is positioned
        """
        if self._bg_layers is None:
            return 0

        tile_h = 32
        image_h = self.get_layer().get_image().get_height()
        n_tiles = (image_h / tile_h) - 1
        size_h = image_h - (tile_h * n_tiles) if position_up else image_h - tile_h

        rect: pg.Rect = self._bg_layers.get_intern_rect()

        return rect.top - size_h if position_up else rect.bottom - size_h

    def render(self, tela: pg.Surface,
               color: tuple = (255, 255, 255, 255),
               invert_x: bool = False, invert_y: bool = False,
               loop: bool = False):
        if not self._coin_colision:
            self.get_coin().render(tela=tela)
        super().render(tela=tela)
