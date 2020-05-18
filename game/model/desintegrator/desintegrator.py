import pygame as pg

from game.constants import *

from ..layer import BackgroundMap
from .fire import FireDesintegrator


class Desintegrator:
    """

    Parameters
    __________
    background: BackgroundMap
        Colision layer of this object to the checks his position in screen
    """
    def __init__(self, background: BackgroundMap):
        self.top_desintegrator = FireDesintegrator(background, invert_gravity=True)
        self.bottom_desintegrator = FireDesintegrator(background)

        self.make_animations_list()

        self.bottom_desintegrator.pos_x = - self.bottom_desintegrator.current_sprite().get_width()/1.1
        self.bottom_desintegrator.pos_y = background.get_background_rect().top + 10
        self.top_desintegrator.pos_x = self.bottom_desintegrator.pos_x
        self.top_desintegrator.pos_y = background.get_background_rect().top - 30

        self.bottom_desintegrator.curr_height = 100
        self.bottom_desintegrator.curr_width = 15
        self.top_desintegrator.curr_height = self.bottom_desintegrator.curr_height
        self.top_desintegrator.curr_width = self.bottom_desintegrator.curr_width
        self.bottom_desintegrator.set_colision_padding(
            pg.Rect(-75, 0, 45, 0)
        )
        self.top_desintegrator.set_colision_padding(
            pg.Rect(-75, 0, 45, 0)
        )
        self._maximum_x: int = 0

    def loaded(self) -> bool:
        """
        :return: bool value, true if this object as ready to be rendenized in screen
        """
        return self.top_desintegrator.loaded() and self.bottom_desintegrator.loaded()

    def update(self):
        """
        Updates the current status of desintegrator
        """
        self.top_desintegrator.update()
        self.bottom_desintegrator.update()
        if self._maximum_x > 0:
            self.top_desintegrator.pos_x += 1
            self.bottom_desintegrator.pos_x += 1
            self._maximum_x = self._maximum_x - 1

    def render(self, tela: pg.Surface):
        """
        Render the desintegrator at screen Surface,

        :param tela: Surface screen frame
        """
        if tela is None or not self.loaded():
            return

        if get_render_type().get('COLISION'):
            pg.draw.ellipse(tela, RED, self.to_rect(), 3)
        if get_render_type().get('NORMAL'):
            self.top_desintegrator.render(tela=tela, color=RED)
            self.bottom_desintegrator.render(tela=tela, color=YELLOW)

    def to_rect(self) -> pg.Rect:
        """
        :return: the desintegrator pg.Rect colision
        """
        rect1 = self.top_desintegrator.to_rect()
        rect2 = self.bottom_desintegrator.to_rect()
        return pg.rect.Rect(
            rect1.x,
            rect1.y,
            rect2.width,
            rect2.bottom
        )

    def make_animations_list(self):
        """
        build the animations of top_desintegrator and bottom_desintegrator
        """
        self.top_desintegrator.make_animations_list()
        self.bottom_desintegrator.make_animations_list()

    def increment_maximum_x_in(self, more: int = 15):
        """
        :param more: value will be incremented in x axis of desintegrator
        """
        self._maximum_x = self._maximum_x + more
