from abc import ABC
from typing import List
import pygame as pg

from .entity_animation import EntityAnimation
import game.model.image as img


class SpriteSheetEntity(EntityAnimation, ABC):
    """
    Abstract Class
    ______________

    Represents the basic components that make up an animated entity
    in motion with animation on the layer
    """

    def __init__(self, file: str, invert_x: bool = False, invert_y: bool = False):
        super().__init__()
        assert (file is not None), 'File necessita do nome do arquivo'
        self.sprite_sheet: img.GameImage = img.load(file)
        self.invert_x: bool = invert_x
        self.invert_y: bool = invert_y
        self._up = False
        self._down = False

    def build(self,
              t_width: int, t_height: int,
              cols: int = 0, rows: int = 0,
              i_x: int = 0, i_y: int = 0,
              jmp_p_x: int = 0, jmp_p_y: int = 0,
              invert_x=None, invert_y=None) -> List[List[pg.SurfaceType]]:
        """
        Build a sprite sheet matrix from a image

        :param t_width: width of a sprite from this sprite sheet
        :param t_height: height of a sprite from this sprite sheet
        :param cols: number of columns that sprite sheet image
        :param rows: number of rows that sprite sheet image
        :param i_x: initial x position from sprite sheet of the first selected sprite
        :param i_y: initial y position from sprite sheet of the first selected sprite
        :param jmp_p_x: jump pixel x in sprite row
        :param jmp_p_y: jump pixel y in sprite column
        :param invert_x: if the sprite sheet x axis is inverted
        :param invert_y: if the sprite sheet y axis is inverted
        :return: a matrix of sprites that will represents a animations frames
        """
        assert (cols > 0) and (t_height > 0 and t_width > 0)

        s_list: List[List[pg.SurfaceType]] = []

        for row in range(rows):
            s_list.append([])
            for col in range(cols):
                s_list[row].append(self.sprite_sheet.get_especifc_frame(
                    x=(i_x + (col * t_width) + (col * jmp_p_x)),
                    y=(i_y + (row * t_height) + (row * jmp_p_y)),
                    width=t_width, height=t_height,
                    invert_x=self.invert_x if (invert_x is None) else invert_x,
                    invert_y=self.invert_y if (invert_y is None) else invert_y
                ))
        return s_list

    @staticmethod
    def sprite_list(from_list: List[List[pg.SurfaceType]],
                    from_row=0, from_i=0, to_i=0,
                    to_row=0, to_col=0) -> List[pg.SurfaceType]:
        """
        Builds a list of sprites that will be composed a animation frame

        :param from_list: matrix of sprites
        :param from_row: selected initial row
        :param from_i: initial position image of list frame
        :param to_i: final position image of list frame
        :param to_row: final selected row of matrix sprites
        :param to_col: final column of matrix sprites
        :return: list of sprites
        """
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
        """
        :return: true if image is fallin in y axis
        """
        return self._down

    def is_jumping(self) -> bool:
        """
        :return: true if image is going up in y axis
        """
        return self._up

    def do_jump(self):
        """make image will going up in y axis"""
        self._up = True

    def do_fall(self):
        """make image will fallin in y axis"""
        self._down = True

    def stop_fall(self):
        """stops image ride down in y axis"""
        self._down = False

    def stop_jump(self):
        """stops image ride up in y axis"""
        self._up = False
