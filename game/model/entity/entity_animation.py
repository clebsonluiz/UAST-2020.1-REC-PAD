from typing import List
from abc import ABC, abstractmethod
import pygame as pg

from .animation import Animation


class EntityAnimation(ABC):
    """
    EntityAnimation Abstract Class
    ______________________________
    Represents a animations of a entity in positioned at screen

    Parameters
    __________
    curr_width : int, optional
        Width of rect colision entity (Default value is a first frame size width)
    curr_height : int, optional
        Height of rect colision entity (Default value is a first frame size height)
    """

    def __init__(self, curr_width: int = 0, curr_height: int = 0):
        self.animacoes: List[Animation] = []
        self.pos_x: float = 0
        self.pos_y: float = 0
        self._vec_x: float = 0
        self._vec_y: float = 0
        self._curr_row: int = 0
        self.curr_width: int = curr_width
        self.curr_height: int = curr_height

    def insert(self, frames: List[pg.SurfaceType], loop: bool = True):
        """
        Inserts a new animation frames to the list
        
        :param frames: list of images the will be composed a animation of entity
        :param loop: if this animations will loop on update method call
        """
        self.animacoes.append(Animation(frames=frames, loop=loop))

    def get_position(self) -> tuple:
        """
        :return: position in screen of entity as tuple (x, y)
        """
        return self.pos_x, self.pos_y

    def set_position(self, position_xy: tuple):
        """
        :param position_xy: respective a tuple (x , y)
        """
        self.pos_x = position_xy[0]
        self.pos_y = position_xy[1]

    def get_vector(self) -> tuple:
        """
        :return: vector as tuple of current directions where entity is moved
        """
        return self._vec_x, self._vec_y

    def get_dy(self) -> float:
        """
        :return: float of vector direction y because x is not used to animation in x or -x
        """
        return self._vec_y

    def get_dx(self) -> float:
        """
        :return: float of vector direction x because x is not used to animation in x or -x
        """
        return self._vec_x

    def set_dy(self, y: float):
        """
        :param y: direction on y axis where entity is moved
        """
        self._vec_y = y

    def set_dx(self, x: float):
        """
        :param x: direction on x axis where entity is moved
        """
        self._vec_x = x

    def sum_dy(self, y: float):
        """
        Used because a weird problem with sum of floats in self._vec_y += y ¯\\_(ツ)_/¯

        :param y: basicaly current y axis = current y axis + y direction
        """
        self._vec_y = sum([self._vec_y, y])

    def sum_dx(self, x: float):
        """
        Used because a weird problem with sum of floats in self._vec_x += y ¯\\_(ツ)_/¯

        :param x: basicaly current x axis = current x axis + x direction
        """
        self._vec_y = sum([self._vec_x, x])

    def to_rect(self, x: float = None, y: float = None) -> pg.Rect:
        """
        Generates a colison pygame rect of a entity

        :return: a pygame Rect with xy positions and size
        """
        x = self.pos_x if (x is None) else x
        y = self.pos_y if (y is None) else y

        if self.curr_height is 0:
            self.curr_height = self.current_sprite().get_height()
        if self.curr_width is 0:
            self.curr_width = self.current_sprite().get_width()
        return pg.rect.Rect(x, y, self.curr_width, self.curr_height)

    def set_curr_row(self, curr_row: int = 0):
        """
        :param curr_row: Current animation that will be animated
        """
        if curr_row >= len(self.animacoes) or curr_row < 0:
            curr_row = len(self.animacoes) - 1
        if curr_row is not self._curr_row:
            self.animacoes[curr_row].reset()
        self._curr_row = curr_row

    def current_sprite(self) -> pg.Surface:
        """
        :return: Current image of the current animation
        that will be rendered in screen
        """
        return self.animacoes[self._curr_row].get_frame()

    @abstractmethod
    def loaded(self) -> bool:
        """
        :return: true if this object with animations is ready to be renderized
        """
        return False

    def update(self):
        """
        Update frames of the current animation
        """
        if not self.loaded():
            return
        self.animacoes[self._curr_row].update()
