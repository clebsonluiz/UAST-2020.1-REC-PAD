from typing import List
import pygame as pg

from game.model.map import BackgroundMap
from game.model.sprite_sheet import SpriteSheet


class Player(SpriteSheet):

    def __init__(self, background: BackgroundMap, invert_gravity: bool = False):
        super().__init__('MS6_Hunter_Walker(Edited).png', invert_x=True)
        self._loaded = False
        self._col_top: bool = False
        self._col_bottom: bool = False
        self._g_inverted: bool = invert_gravity
        self._bg = background

    def _jump_starts(self) -> float:
        return self._g_value() * -5.5

    def _stop_jump_speed(self) -> float:
        return self._g_value() * 0.4

    def _fall_speed(self) -> float:
        return self._g_value() * 0.3

    def _max_fall_speed(self) -> float:
        return self._g_value() * 10.0

    def _g_value(self) -> float:
        return -1.0 if self._g_inverted else 1.0

    def change_gravit(self):
        self._g_inverted = (not self._g_inverted)

    def is_dy_less_or_inverted_than(self, less_than: float = 0.0, greater_than: float = 0.0) -> bool:
        return (self.get_dy() < less_than) if not self._g_inverted else (self.get_dy() > greater_than)

    def is_dy_greater_or_inverted_than(self, greater_than: float = 0.0, less_than: float = 0.0) -> bool:
        return (self.get_dy() > greater_than) if not self._g_inverted else (self.get_dy() < less_than)

    def _calc_colision(self, x, y):
        self._col_top = self.to_rect(x=x, y=y).colliderect(self._bg.get_limit_top())
        self._col_bottom = self.to_rect(x=x, y=y).colliderect(self._bg.get_limit_bottom())

    def _check_map_colision(self):
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

        if self.is_dy_greater_or_inverted_than():
            if not self.is_falling():
                self.do_fall()
        elif self.is_dy_less_or_inverted_than():
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
        self.set_curr_row(curr_row=self._get_animation_row())
        super().update()

    def render(self, tela: pg.Surface, color: tuple = (255, 255, 255, 255)):
        if tela is None:
            return
        if color is not None:
            self.current_sprite().fill(color=color, special_flags=pg.BLEND_RGBA_MIN)
        self.invert_y = self._g_inverted
        image = pg.transform.flip(self.current_sprite(), not self.invert_x, self.invert_y,)
        tela.blit(image, self.get_position())

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

        self.insert(s_list_walking)
        self.insert(s_list_jumping, False)
        self.insert(s_list_falling, False)
        self._loaded = True

    @staticmethod
    def swich_positions_player_shadow(player: SpriteSheet, shadow: SpriteSheet):
        player_position: tuple = player.get_position()
        shadow_position: tuple = shadow.get_position()
        player.set_position(shadow_position)
        shadow.set_position(player_position)
