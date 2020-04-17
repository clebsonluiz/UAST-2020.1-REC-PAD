from typing import List
from random import randint as next_int
import pygame as pg
from game.constants import *
from game.model.map.obstacle import Obstacle


class BackgroundMap:
    """
    TEMP Class
    __________
    Will be changed
    """

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
