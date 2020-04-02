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
        self._gravit_change: bool = False
        self._background = background

    def _jump_starts(self) -> float:
        return self._get_gravit() * -5.5

    def _stop_jump_speed(self) -> float:
        return self._get_gravit() * 0.4

    def _fall_speed(self) -> float:
        return self._get_gravit() * 0.3

    def _max_fall_speed(self) -> float:
        return self._get_gravit() * 8.0

    def _get_gravit(self) -> float:
        return -1.0 if self._gravit_change else 1.0

    def change_gravit(self):
        self._gravit_change = (not self._gravit_change)

    def _calc_colision(self, x, y):
        self._col_top = self.to_rect(x=x, y=y).colliderect(self._background.get_limit_top())
        self._col_bottom = self.to_rect(x=x, y=y).colliderect(self._background.get_limit_bottom())

    def _check_map_colision(self):
        if self._background is None:
            return

        ydest = self.pos_y + self.get_vec_y()
        ytemp = self.pos_y
        self._calc_colision(self.pos_x, ydest)
        if self.get_vec_y() < 0.0:
            if self._col_top:
                self.set_vec_y(0.0)
                if self._gravit_change:
                    self.stop_fall()
            else:
                ytemp += self.get_vec_y()
        if self.get_vec_y() > 0.0:
            if self._col_bottom:
                self.set_vec_y(0.0)
                if not self._gravit_change:
                    self.stop_fall()
            else:
                ytemp += self.get_vec_y()

        if not self.is_falling():
            self._calc_colision(self.pos_x, ydest + self._get_gravit())
            if (not self._col_top) if self._gravit_change else (not self._col_bottom):
                self.do_fall()

        self.pos_y = ytemp

    def _next_position(self):
        if self.is_jumping() and (not self.is_falling()):
            self.set_vec_y(self._jump_starts())
            self.do_fall()

        if self.is_falling():
            self.sum_vec_y(self._fall_speed())
            if self.get_vec_y() < 0.0 if self._gravit_change else self.get_vec_y() > 0.0:
                self.stop_jump()
            if  (self.get_vec_y() > 0.0) if self._gravit_change else (self.get_vec_y() < 0.0) and (not self.is_jumping()):
                self.sum_vec_y(self._stop_jump_speed())
            if self.get_vec_y() < self._max_fall_speed() if self._gravit_change else self.get_vec_y() > self._max_fall_speed():
                self.set_vec_y(self._max_fall_speed())

    def _next_move(self):

        if (self.get_vec_y() < 0.0) if self._gravit_change else (self.get_vec_y() > 0.0):
            if not self.is_falling():
                self.do_fall()
        elif (self.get_vec_y() > 0.0) if self._gravit_change else (self.get_vec_y() < 0.0):
            if not self.is_jumping():
                self.do_jump()

    def _get_animation_row(self) -> int:
        if self.is_jumping():
            return 4 if self._gravit_change else 1
        elif self.is_falling():
            return 5 if self._gravit_change else 2
        return 3 if self._gravit_change else 0

    def loaded(self) -> bool:
        return self._loaded

    def update(self):
        self._next_position()
        self._check_map_colision()
        self._next_move()
        self.set_curr_row(curr_row=self._get_animation_row())
        super().update()

    def make_animations_list(self):
        s_matrix_walking = self.build(
            t_width=63, t_height=39,
            cols=11, rows=1,
            i_x=10, i_y=240,
            jmp_p_x=2, jmp_p_y=0
        )
        s_matrix_jumping_falling = self.build(
            t_width=37, t_height=46,
            cols=9, rows=2,
            i_x=10, i_y=94,
            jmp_p_x=12, jmp_p_y=18
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

        s_matrix_walking_2 = self.build(
            t_width=63, t_height=39,
            cols=11, rows=1,
            i_x=10, i_y=240,
            jmp_p_x=2, jmp_p_y=0, invert_y=True
        )
        s_matrix_jumping_falling_2 = self.build(
            t_width=37, t_height=46,
            cols=9, rows=2,
            i_x=10, i_y=94,
            jmp_p_x=12, jmp_p_y=18, invert_y=True
        )
        s_list_walking_2 = SpriteSheet.sprite_list(
            from_list=s_matrix_walking_2,
            from_row=0, from_i=0, to_i=11,
        )
        s_list_jumping_2 = SpriteSheet.sprite_list(
            from_list=s_matrix_jumping_falling_2,
            from_row=0, from_i=0, to_i=9,
        )
        s_list_falling_2 = SpriteSheet.sprite_list(
            from_list=s_matrix_jumping_falling_2,
            from_row=0, from_i=9, to_i=18,
        )

        self.insert(s_list_walking)
        self.insert(s_list_jumping, False)
        self.insert(s_list_falling, False)
        self.insert(s_list_walking_2)
        self.insert(s_list_jumping_2, False)
        self.insert(s_list_falling_2, False)
        self._loaded = True
