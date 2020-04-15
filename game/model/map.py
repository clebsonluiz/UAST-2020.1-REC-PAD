from typing import List
from random import randint as next_int
import pygame as pg
from game.constants import *


class Obstacle:

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


class BackgroundMap:

    def __init__(self):
        self._rect_top = pg.rect.Rect(0, SCREEN_HEIGHT * 0.2, SCREEN_WIDTH, 10)
        self._rect_bottom = pg.rect.Rect(0, SCREEN_HEIGHT * 0.7, SCREEN_WIDTH, 10)
        self._obstacles: List[Obstacle] = []
        self._default_lenths: List[int] = [20, 50, 100]

        self._obstacles.append(self._generate_an_obstacle_at(position=0))
        self._obstacles.append(self._generate_an_obstacle_at(position=1))
        self._obstacles.append(self._generate_an_obstacle_at(position=1))

    def get_background_rect(self) -> pg.Rect:
        x: float = 0.0
        y: float = self.get_limit_top().bottom
        width: float = SCREEN_WIDTH
        height: float = self.get_limit_bottom().top - self.get_limit_top().bottom
        return pg.Rect(x, y, width, height)

    def get_limit_top(self) -> pg.Rect:
        return self._rect_top

    def get_limit_bottom(self) -> pg.Rect:
        return self._rect_bottom

    def _distance_from_another(self) -> int:
        # dist = next_int(200, 500)
        dist = 200
        if len(self._obstacles) is 0:
            return SCREEN_WIDTH
        else:
            return self._obstacles[-1].get_last_distance(default=dist)

    def _position_y(self, position: int) -> int:
        if position is 0:
            return self._rect_top.y + self._rect_top.h
        else:
            return self._rect_bottom.y - 20

    def _generate_width(self):
        return self._default_lenths[next_int(0, 2)]

    def _generate_an_obstacle_at(self, position: int = 0) -> Obstacle:
        obs: Obstacle = Obstacle(x=self._distance_from_another(),
                                 y=self._position_y(position=position),
                                 dx=-5.0, dy=0.0,
                                 width=self._generate_width(), height=20)
        return obs

    def get_obstacles(self) -> List[Obstacle]:
        return self._obstacles

    def update(self, speed: float = 1.0):
        if len(self._obstacles) is 0:
            return
        if len(self._obstacles) <= 5:
            self._obstacles.append(self._generate_an_obstacle_at(position=1))
        if self._obstacles[0].is_out_screen():
            self._obstacles.pop(0)
        for e in self._obstacles:
            e.update(speed=speed)
