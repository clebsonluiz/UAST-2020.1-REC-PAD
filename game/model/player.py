from typing import List
import pygame as pg
from game.model.sprite_sheet import SpriteSheet


class Player(SpriteSheet):

    def __init__(self):
        super().__init__('MS6_Hunter_Walker(Edited).png')
        self.animacoes: List[List[pg.SurfaceType]] = []
        self._loaded = False
        self._curr_row: int = 0
        self._curr_col: int = 0

    def get_sprite(self, row=0, col=0):
        if len(self.sprites) <= 0:
            self.insert_list(
                t_width=63, t_height=39,
                cols=11, rows=1,
                i_x=10, i_y=240,
                jmp_p_x=2, jmp_p_y=0
            )
        return super().get_sprite(row=row, col=col)

    def loaded(self) -> bool:
        return self._loaded

    def make_animations_list(self):
        s_matrix_walking = self.build(
            t_width=63, t_height=39,
            cols=11, rows=1,
            i_x=10, i_y=240,
            jmp_p_x=2, jmp_p_y=0
        )
        s_matrix_jumping_falling = self.build(
            t_width=37, t_height=62,
            cols=9, rows=2,
            i_x=10, i_y=94,
            jmp_p_x=12, jmp_p_y=0
        )
        s_list_walking = self.sprite_list(
            from_list=s_matrix_walking,
            from_row=0, from_i=0, to_i=11,
        )
        s_list_jumping = self.sprite_list(
            from_list=s_matrix_jumping_falling,
            from_row=0, from_i=0, to_i=9,
        )
        s_list_falling = self.sprite_list(
            from_list=s_matrix_jumping_falling,
            from_row=0, from_i=9, to_i=18,
        )
        self.animacoes.append(s_list_walking)
        self.animacoes.append(s_list_jumping)
        self.animacoes.append(s_list_falling)
        self._loaded = True

    def set_curr_row(self, curr_row: int = 0):
        if curr_row >= len(self.animacoes) or curr_row < 0:
            curr_row = len(self.animacoes) - 1
        self._curr_row = curr_row

    def current_sprite(self) -> pg.SurfaceType:
        return self.animacoes[self._curr_row][self._curr_col]

    def update(self):
        if not self.loaded():
            return
        self._curr_col += 1
        if self._curr_col >= len(self.animacoes[self._curr_row]):
            self._curr_col = 0