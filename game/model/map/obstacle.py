import pygame as pg


class Obstacle:
    """
    TEMP Class
    __________
    Will be changed
    """
    def __init__(self, x=0.0, y=0.0, dx=0.0, dy=0.0, width=0, height=0):
        self._pos_x: float = x
        self._pos_y: float = y
        self._vec_x: float = dx
        self._vec_y: float = dy
        self._curr_width = width
        self._curr_height = height

    def get_position(self) -> tuple:
        return self._pos_x, self._pos_y

    def get_vector(self) -> tuple:
        return self._vec_x, self._vec_y

    def set_vector(self, dx: float = 0.0, dy: float = 0.0):
        self._vec_x = dx
        self._vec_y = dy

    def get_curr_width(self) -> int:
        return self._curr_width

    def get_curr_height(self) -> int:
        return self._curr_height

    def get_last_distance(self, default: int = 100) -> int:
        return int(self._pos_x + self._curr_width * 2) + default

    def to_rec(self) -> pg.Rect:
        return pg.rect.Rect(self._pos_x, self._pos_y, self._curr_width, self._curr_height)

    def is_out_screen(self) -> bool:
        return (self._pos_x + self._curr_width) <= 0.0

    def update(self, speed: float = 1):
        if self._pos_x >= 0.0:
            self._pos_x += self._vec_x * speed
            self._pos_y += self._vec_y * speed
        else:
            self._curr_width -= abs(int(self._vec_x * speed))
