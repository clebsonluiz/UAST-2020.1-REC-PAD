from typing import List
import pygame as pg

from game.model.map import BackgroundMap
from game.model.sprite_sheet import SpriteSheet


class Player(SpriteSheet):

    def __init__(self, background: BackgroundMap):
        super().__init__('MS6_Hunter_Walker(Edited).png', invert_x=True)
        self._loaded = False
        self._col_top: bool = False
        self._col_bottom: bool = False
        self._background = background
        self._jump_starts: float = -5.5
        self._stop_jump_speed: float = 0.3
        self._fall_speed: float = 0.2
        self._max_fall_speed: float = 4.0

    def _calc_colision(self, x, y):
        self._col_top = self.to_rect(x=x, y=y).colliderect(self._background.get_limit_top())
        self._col_bottom = self.to_rect(x=x, y=y).colliderect(self._background.get_limit_bottom())

    def _check_map_colision(self):
        if self._background is None:
            return

        ydest = self.pos_y + self.vec_y
        ytemp = self.pos_y

        self._calc_colision(self.pos_x, ydest)
        if self.vec_y < 0:
            if self._col_top:
                self.vec_y = 0
            else:
                ytemp += self.vec_y
        if self.vec_y > 0:
            if self._col_bottom:
                self.vec_y = 0
                self.stop_fall()
            else:
                ytemp += self.vec_y

        if not self.is_falling():
            self._calc_colision(self.pos_x, ydest + 1)
            if not self._col_bottom:
                self.do_fall()

        self.pos_y = ytemp

    def _next_position(self):
        if self.is_jumping() and (not self.is_falling()):
            self.vec_y = self._jump_starts
            self.do_fall()

        if self.is_falling():
            self.vec_y += self._fall_speed
            if self.vec_y > 0:
                self.stop_jump()
            if self.vec_y < 0 and (not self.is_jumping()):
                self.vec_y += self._stop_jump_speed
            if self.vec_y > self._max_fall_speed:
                self.vec_y = self._max_fall_speed

    def _next_move(self):
        if self.vec_y > 0:
            if not self.is_falling():
                self.do_fall()
        elif self.vec_y < 0:
            if not self.is_jumping():
                self.do_jump()

    def _get_animation_row(self) -> int:
        if self.is_jumping():
            return 1
        elif self.is_falling():
            return 2
        return 0

    def loaded(self) -> bool:
        return self._loaded

    def update(self):
        self._next_position()
        self._check_map_colision()
        self._next_move()
        row = self._get_animation_row()
        self.set_curr_row(curr_row=row)
        super().update()

    def make_animations_list(self):
        s_matrix_walking = self.build(
            t_width=63, t_height=39,
            cols=11, rows=1,
            i_x=10, i_y=240,
            jmp_p_x=2, jmp_p_y=0
        )
        s_matrix_jumping_falling = self.build(
            t_width=37, t_height=50,
            cols=9, rows=2,
            i_x=10, i_y=94,
            jmp_p_x=12, jmp_p_y=14
        )
        s_list_walking = SpriteSheet.sprite_list(
            from_list=s_matrix_walking,
            from_row=0, from_i=0, to_i=11,
        )
        s_list_jumping = SpriteSheet.sprite_list(
            from_list=s_matrix_jumping_falling,
            from_row=0, from_i=0, to_i=9,
        )
        s_list_falling = SpriteSheet.sprite_list(
            from_list=s_matrix_jumping_falling,
            from_row=0, from_i=9, to_i=18,
        )

        self.insert(s_list_walking)
        self.insert(s_list_jumping, False)
        self.insert(s_list_falling, False)
        self._loaded = True
