from typing import List
import pygame as pg
from game.constants import *


class BackgroundMap:

    def __init__(self):
        self._rect_top = pg.rect.Rect(0, SCREEN_HEIGHT * 0.1, SCREEN_WIDTH, 5)
        self._rect_bottom = pg.rect.Rect(0, SCREEN_HEIGHT * 0.7, SCREEN_WIDTH, 5)

    def get_limit_top(self) -> pg.Rect:
        return self._rect_top

    def get_limit_bottom(self) -> pg.Rect:
        return self._rect_bottom
