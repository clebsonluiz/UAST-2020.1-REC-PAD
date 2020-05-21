import pygame as pg
from abc import ABC, abstractmethod

from .sprite_sheet import SpriteSheetEntity


class EntityMap(SpriteSheetEntity, ABC):

    """
    Class of a entity map that will be rendenized in screen.
    Inspired by (Java tutorial Game from ForeignGuyMike)
    """
    def __init__(self, file: str, background,
                 invert_gravity: bool = False,
                 invert_x: bool = False):
        super().__init__(file=file, invert_x=invert_x)
        from ..layer import BackgroundMap
        self._loaded = False
        self._col_top: bool = False
        self._col_bottom: bool = False
        self._g_inverted: bool = invert_gravity
        self._bg: BackgroundMap = background

    def _jump_starts(self) -> float:
        """
        :return: value will be used to make the movement of jump
        """
        return self._g_value() * -5.5

    def _stop_jump_speed(self) -> float:
        """
        :return: value will be used to make the stop jump movement
        """
        return self._g_value() * 0.3

    def _fall_speed(self) -> float:
        """
        :return: value will be used to make the speed of falling after jump
        """
        return self._g_value() * 0.25

    def _max_fall_speed(self) -> float:
        """
        :return: value will be used to make the movement of jump
        """
        return self._g_value() * 10.0

    def _g_value(self) -> float:
        """
        :return: value will be used to represents the object gravit direction
        """
        return -1.0 if self._g_inverted else 1.0

    def change_gravit(self):
        """change the current graviti to the oposite"""
        self._g_inverted = (not self._g_inverted)

    def is_dy_less_or_inverted_than(self, less_than: float = 0.0, greater_than: float = 0.0) -> bool:
        """
        :return: bool value for the verification
        """
        return (self.get_dy() < less_than) if not self._g_inverted else (self.get_dy() > greater_than)

    def is_dy_greater_or_inverted_than(self, greater_than: float = 0.0, less_than: float = 0.0) -> bool:
        """
        :return: bool value for the verification
        """
        return (self.get_dy() > greater_than) if not self._g_inverted else (self.get_dy() < less_than)

    def _calc_colision(self, x, y):
        """
        calcs the colision box to check if movement will be continued
        """
        self._col_top = self.to_rect(x=x, y=y).colliderect(self._bg.get_limit_top())
        self._col_bottom = self.to_rect(x=x, y=y).colliderect(self._bg.get_limit_bottom())

    def _check_map_colision(self):
        """
        makes the check of colision and movement of player
        """
        if self._bg is None:
            return

        ydest = self.pos_y + self.get_dy()
        ytemp = self.pos_y
        self._calc_colision(self.pos_x, ydest)
        if self.get_dy() < 0.0:
            if self._col_top:
                self.set_dy(0.0)
                if self._g_inverted:
                    self.stop_fall()
            else:
                ytemp += self.get_dy()
        if self.get_dy() > 0.0:
            if self._col_bottom:
                self.set_dy(0.0)
                if not self._g_inverted:
                    self.stop_fall()
            else:
                ytemp += self.get_dy()

        if not self.is_falling():
            self._calc_colision(self.pos_x, ydest + self._g_value())
            if (not self._col_top) if self._g_inverted else (not self._col_bottom):
                self.do_fall()

        self.pos_y = ytemp

    def _next_position(self):
        """
        make the next position of player when the events is dispared
        """
        if self.is_jumping() and (not self.is_falling()):
            self.set_dy(self._jump_starts())
            self.do_fall()

        if self.is_falling():
            self.sum_dy(self._fall_speed())
            if self.is_dy_greater_or_inverted_than():
                self.stop_jump()
            if self.is_dy_less_or_inverted_than() and (not self.is_jumping()):
                self.sum_dy(self._stop_jump_speed())
            if self.get_dy() < self._max_fall_speed() if self._g_inverted else self.get_dy() > self._max_fall_speed():
                self.set_dy(self._max_fall_speed())

    def _next_move(self):
        """
        checks if is necessery to do a jump or fall, on current check value of y axis vector
        """
        if self.is_dy_greater_or_inverted_than():
            if not self.is_falling():
                self.do_fall()
        elif self.is_dy_less_or_inverted_than():
            if not self.is_jumping():
                self.do_jump()

    @abstractmethod
    def get_animation_row(self) -> int:
        """
        :return: int value of a animation to be executed in event check
        """
        return 0

    def loaded(self) -> bool:
        """
        :return: bool value that represents if this object is ready to be rendenized
        """
        return self._loaded

    def super_update(self):
        super().update()

    def update(self):
        """
        update the current object status
        """
        self._next_position()
        self._check_map_colision()
        self._next_move()
        self.set_curr_row(curr_row=self.get_animation_row())
        self.super_update()

    def render(self, tela: pg.Surface, color: tuple = (255, 255, 255, 255), opacity: int = None):
        """
        render this object at screen frame (tela)

        :param tela: Surface of screen that object will be drawed
        :param color: tuple of primary color of image
        :param opacity: int value of opacity of image
        """
        if tela is None:
            return
        if color is not None:
            self.current_sprite().fill(color=color, special_flags=pg.BLEND_RGBA_MIN)
        self.invert_y = self._g_inverted
        image = pg.transform.flip(self.current_sprite(), not self.invert_x, self.invert_y,).convert()
        if opacity:
            EntityMap.blit_alpha(target=tela, source=image, location=self.get_position(), opacity=opacity)
        else:
            tela.blit(image, self.get_position())

    @abstractmethod
    def make_animations_list(self):
        """
        build the list of animations of this entity
        """
        self._loaded = True

    @staticmethod
    def blit_alpha(target: pg.Surface, source: pg.SurfaceType, location: tuple, opacity: int):
        """
        :param target: Screen frame
        :param source: original image
        :param location: drawer location
        :param opacity: opacity of the new image
        """
        x = location[0]
        y = location[1]
        temp: pg.Surface = pg.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)
