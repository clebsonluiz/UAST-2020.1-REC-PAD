from typing import List
import pygame as pg
from game.model.sprite_sheet import SpriteSheet


class Player(SpriteSheet):

    def __init__(self):
        super().__init__('MS6_Hunter_Walker(Edited).png', invert_x=True)
        self._loaded = False

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

        self.insert(s_list_walking)
        self.insert(s_list_jumping, False)
        self.insert(s_list_falling, False)
        self._loaded = True
