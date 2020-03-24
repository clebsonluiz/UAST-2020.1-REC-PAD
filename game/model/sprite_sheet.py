from typing import List

import pygame as pg
from game.constants import *


class SpriteSheet:

    def __init__(self, file: str):
        assert (file is not None), 'File necessita do nome do arquivo'
        self.sprite_sheet = pg.image.load(ASSETS_PATH + 'images/' + file)
        self.sprites: List[List[pg.SurfaceType]] = []

    def insert_list(self, t_width: int, t_height: int,
                    cols: int = 0, rows: int = 0,
                    i_x: int = 0, i_y: int = 0,
                    jmp_p_x: int = 0, jmp_p_y: int = 0):
        self.sprites.extend(self.build(t_width=t_width, t_height=t_height,
                                       cols=cols, rows=rows,
                                       i_x=i_x, i_y=i_y,
                                       jmp_p_x=jmp_p_x,
                                       jmp_p_y=jmp_p_y))

    def build(self,
              t_width: int, t_height: int,
              cols: int = 0, rows: int = 0,
              i_x: int = 0, i_y: int = 0,
              jmp_p_x: int = 0, jmp_p_y: int = 0) -> List[List[pg.SurfaceType]]:
        assert (cols > 0) and (t_height > 0 and t_width > 0)

        s_list: List[List[pg.SurfaceType]] = []

        for row in range(rows):
            s_list[row] = []
            for col in range(cols):
                s_list[row].append(self.get_image_from_sh(
                    x=(i_x + (col * t_width) + (col * jmp_p_x)),
                    y=(i_y + (row * t_width) + (row * jmp_p_y)),
                    width=t_width, height=t_height,
                ))
        return s_list

    def get_image_from_sh(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        image = pg.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image

    def get_sprite(self, row=0, col=0):
        return self.sprites[row][col]

    def sprite_list(self,
                    from_row=0, from_i=0, to_i=0,
                    to_row=0, to_col=0) -> List[pg.SurfaceType]:
        if to_row is 0:
            to_row = len(self.sprite_sheet) - 1
        if to_col is 0:
            to_col = len(self.sprite_sheet[to_row]) - 1

        assert (
            (from_row is not None) and (to_row is not None) and
            (to_col is not None) and (to_row >= from_row),
            'Não existe um indice de imagens válido definido'
        )

        s_list = []

        for row in range((to_row + 1)):
            if row == to_row:
                s_list.extend(self.sprite_sheet[row][:to_col])
            else:
                s_list.extend(self.sprite_sheet[row])

        return s_list[from_i: to_i]
