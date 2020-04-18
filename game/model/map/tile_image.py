import game.model.image as img
from typing import List
import pygame as pg


class TileImage:
    """
    Class used to make the tile sheet image on will build the surface screen
    """

    def __init__(self):
        self._tile_image = img.load("platformtiles_from_OpenGameArt_by_Lanea Zimmerman.png")
        self._tiles: List[List[img.GameImage]] = self._build(tile_width=32, tile_height=32, cols=8, rows=3)

    def get_tile(self, row: int = 0, col: int = 0) -> img.GameImage:
        """
        :param row: row when tile is
        :param col: column when tile is
        :return: GameImage tile in the tile in current row and column
        """
        return self._tiles[row][col]

    def _build(self,
               tile_width: int, tile_height: int,
               cols: int = 0, rows: int = 0,
               i_x: int = 0, i_y: int = 0,
               jmp_p_x: int = 0, jmp_p_y: int = 0, ) -> List[List[img.GameImage]]:
        """
        Build a tile image matrix from a original image

        :param tile_width: width of tile from this tile image
        :param tile_height: height of tile from this tile image
        :param cols: number of columns that tile image
        :param rows: number of rows that tile image
        :param i_x: initial x position from tile image of the first selected tile
        :param i_y: initial y position from tile image of the first selected tile
        :param jmp_p_x: jump pixel x in tile image row
        :param jmp_p_y: jump pixel y in tile image column
        :return: a matrix of sprites that will represents a animations frames
        """
        assert (cols > 0) and (tile_height > 0 and tile_width > 0)

        s_list: List[List[img.GameImage]] = []

        for row in range(rows):
            s_list.append([])
            for col in range(cols):
                s_list[row].append(img.GameImage.from_pygame_surface(
                    self._tile_image.get_especifc_frame(
                        x=(i_x + (col * tile_width) + (col * jmp_p_x)),
                        y=(i_y + (row * tile_height) + (row * jmp_p_y)),
                        width=tile_width, height=tile_height,
                    )))
        return s_list

    def build_surface(self,
                      tiles: List[List[int]], surface: pg.Surface = None,
                      ) -> pg.Surface:
        if surface is None:
            width: int = len(tiles[0]) * self._tiles[0][0].get_image().get_width()
            height: int = len(tiles) * self._tiles[0][0].get_image().get_height()
            surface = pg.Surface([width, height]).convert()
            surface.set_colorkey((0, 0, 0, 255))

        for row in range(len(tiles)):
            for col in range(len(tiles[row])):
                tile = tiles[row][col]
                if tile < 0:
                    break

                r = tile // (len(self._tiles[0]) * 1)
                c = tile % (len(self._tiles[0]) * 1)

                image = self._tiles[r][c].get_image()
                xdest: int = image.get_width() * col
                ydest: int = image.get_height() * row

                surface.blit(image, (xdest, ydest))
        return surface
