from abc import ABC
from typing import List

import pygame as pg
from game.constants import *
from game.model.spritesheetanimation import SpriteSheetAnimation


class SpriteSheet(SpriteSheetAnimation, ABC):

    def __init__(self, file: str, invert_x: bool = False, invert_y: bool = False):
        super().__init__()
        assert (file is not None), 'File necessita do nome do arquivo'
        self.sprite_sheet = pg.image.load(ASSETS_PATH + 'images/' + file)
        self.invert_x: bool = invert_x
        self.invert_y: bool = invert_y
        self._up = False
        self._down = False

    def build(self,
              t_width: int, t_height: int,
              cols: int = 0, rows: int = 0,
              i_x: int = 0, i_y: int = 0,
              jmp_p_x: int = 0, jmp_p_y: int = 0) -> List[List[pg.SurfaceType]]:
        assert (cols > 0) and (t_height > 0 and t_width > 0)

        s_list: List[List[pg.SurfaceType]] = []

        for row in range(rows):
            s_list.append([])
            for col in range(cols):
                s_list[row].append(self.get_image_from_sh(
                    x=(i_x + (col * t_width) + (col * jmp_p_x)),
                    y=(i_y + (row * t_height) + (row * jmp_p_y)),
                    width=t_width, height=t_height,
                ))
        return s_list

    def get_image_from_sh(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        image = pg.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        image = pg.transform.flip(image, self.invert_x, self.invert_y)
        return image

    # def get_sprite(self, row=0, col=0):
    #     return self.animacoes[row][col]

    @staticmethod
    def sprite_list(from_list: List[List[pg.SurfaceType]],
                    from_row=0, from_i=0, to_i=0,
                    to_row=0, to_col=0) -> List[pg.SurfaceType]:

        assert (from_list is not None and len(from_list) > 0)

        if to_row is 0:
            to_row = len(from_list) - 1
        if to_col is 0:
            to_col = len(from_list[to_row])

        s_list = []

        for row in range(from_row, (to_row + 1)):
            if row == to_row:
                s_list.extend(from_list[row][:to_col])
            else:
                s_list.extend(from_list[row])

        return s_list[from_i: to_i]

    def is_falling(self) -> bool:
        return self._down

    def is_jumping(self) -> bool:
        return self._up

    def do_jump(self):
        self._up = True

    def do_fall(self):
        self._down = True

    def stop_fall(self):
        self._down = False

    def stop_jump(self):
        self._up = False
