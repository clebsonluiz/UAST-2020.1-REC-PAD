from typing import List
from abc import ABC, abstractmethod
import pygame as pg


class _Animation:

    def __init__(self, frames: List[pg.SurfaceType], loop: bool = True):
        assert frames is not None and loop is not None
        self.frames: List[pg.SurfaceType] = frames
        self.loop: bool = loop
        self._played: bool = False
        self._curr_col: int = 0

    def get_frame(self) -> pg.SurfaceType:
        return self.frames[self._curr_col]

    def update(self):
        if self._played:
            return
        self._curr_col += 1
        if self._curr_col >= len(self.frames):
            if self.loop:
                self.reset()
            else:
                self._curr_col = len(self.frames) - 1
                self._played = True

    def reset(self):
        self._curr_col = 0
        self._played = False


class SpriteSheetAnimation(ABC):
    
    def __init__(self, curr_width: int = 0, curr_height: int = 0):
        self.animacoes: List[_Animation] = []
        self.pos_x: float = 0
        self.pos_y: float = 0
        self._vec_x: float = 0
        self._vec_y: float = 0
        self._curr_row: int = 0
        self.curr_width: int = curr_width
        self.curr_height: int = curr_height

    def insert(self, frames: List[pg.SurfaceType], loop: bool = True):
        self.animacoes.append(_Animation(frames=frames, loop=loop))

    def get_position(self) -> tuple:
        return self.pos_x, self.pos_y

    def get_vector(self) -> tuple:
        return self._vec_x, self._vec_y

    def get_vec_y(self) -> float:
        return self._vec_y

    def set_vec_y(self, y: float):
        self._vec_y = y

    def sum_vec_y(self, y: float):
        self._vec_y = sum([self._vec_y, y])

    def to_rect(self, x: float = None, y: float = None) -> pg.Rect:
        if x is None:
            x = self.pos_x
        if y is None:
            y = self.pos_y
        if self.curr_height is 0:
            self.curr_height = self.current_sprite().get_height()
        if self.curr_width is 0:
            self.curr_width = self.current_sprite().get_width()

        return pg.rect.Rect(x, y, self.curr_width, self.curr_height)

    def set_curr_row(self, curr_row: int = 0):
        if curr_row >= len(self.animacoes) or curr_row < 0:
            curr_row = len(self.animacoes) - 1
        if curr_row is not self._curr_row:
            self.animacoes[curr_row].reset()
        self._curr_row = curr_row

    def current_sprite(self) -> pg.SurfaceType:
        return self.animacoes[self._curr_row].get_frame()

    # def get_width(self):
    #     if self.curr_width is None:
    #         self.curr_width = self.current_sprite().get_width()
    #     return self.curr_width
    #
    # def get_height(self):
    #     if self.curr_height is None:
    #         self.curr_height = self.current_sprite().get_height()
    #     return self.curr_height

    @abstractmethod
    def loaded(self) -> bool:
        return False

    def update(self):
        if not self.loaded():
            return
        self.animacoes[self._curr_row].update()
