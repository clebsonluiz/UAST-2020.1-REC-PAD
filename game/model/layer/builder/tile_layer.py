import pygame as pg

from typing import List
from ...image import game_image as img
from .tile_image import TileImage


class TileLayer:
    """
    Class TileLayer for build the background layers will render on map

    Parameters
    __________
        tile_map : List[List[float]]
            Matrix of float tiles
        vec_x : float
            x direction when layer is moved
        vec_y : float
            y direction when layer is moved
        invert_x : bool
            inverts the layer image in xAxis
        invert_y : bool
            inverts the layer image in yAxis
    """

    def __init__(self, tile_map: List[List[float]],
                 vec_x: float = 0, vec_y: float = 0,
                 invert_x: bool = False, invert_y: bool = False):
        self._layer: img.GameImage = img.GameImage.from_pygame_surface(
            TileImage().build_surface(tiles=tile_map)
        )
        self.pos_x: float = 0
        self.pos_y: float = 0
        self._vec_x: float = vec_x
        self._vec_y: float = vec_y
        if invert_x or invert_y:
            self._layer.set_image(self._layer.flip(invert_x=invert_x, invert_y=invert_y))

    def get_position(self) -> tuple:
        """
        :return: position in screen of layer as tuple (x, y)
        """
        return self.pos_x, self.pos_y

    def set_position(self, position_xy: tuple):
        """
        :param position_xy: respective a tuple (x , y)
        """
        self.pos_x = position_xy[0]
        self.pos_y = position_xy[1]

    def get_vector(self) -> tuple:
        """
        :return: vector as tuple of current directions where entity is moved
        """
        return self._vec_x, self._vec_y

    def get_dy(self) -> float:
        """
        :return: float of vector direction y because x is not used to animation in x or -x
        """
        return self._vec_y

    def get_dx(self) -> float:
        """
        :return: float of vector direction x because x is not used to animation in x or -x
        """
        return self._vec_x

    def set_dy(self, y: float):
        """
        :param y: direction on y axis where layer is moved
        """
        self._vec_y = y

    def set_dx(self, x: float):
        """
        :param x: direction on x axis where layer is moved
        """
        self._vec_x = x

    def to_rect(self, x: float = None, y: float = None, scale: float = 1.0) -> pg.Rect:
        """
        Generates a colison pygame rect of a layer

        :return: a pygame Rect with xy positions and size
        """
        x = self.pos_x if (x is None) else x
        y = self.pos_y if (y is None) else y
        width = self._layer.get_image().get_width()
        height = self._layer.get_image().get_height()

        return pg.rect.Rect(x * scale, y * scale, width * scale, height * scale)

    def render(self, tela: pg.Surface,
               color: tuple = (255, 255, 255, 255),
               invert_x: bool = False, invert_y: bool = False,
               loop: bool = False):
        """
        render this object at screen frame (tela)

        :param tela: Surface of screen that object will be drawed
        :param color: tuple of primary color of image
        :param loop: if the layer is a looping image background
        :param invert_y: if the y axis is inverted
        :param invert_x: if the x axis is inverted
        """
        if tela is None:
            return
        if color is not None:
            self._layer.get_image().fill(color=color, special_flags=pg.BLEND_RGBA_MIN)

        image = self._layer.flip(invert_x=invert_x, invert_y=invert_y)

        tela.blit(image, self.get_position())
        if loop:
            if self.pos_x < 0:
                tela.blit(image,
                          (self.pos_x + image.get_width(), self.pos_y))
            elif self.pos_x > 0:
                tela.blit(image,
                          (self.pos_x - image.get_width(), self.pos_y))

    def update(self, speed: float = 1.0):
        """
        Used for updates the movement of the layer on map.
        this consideres loop

        :param speed: speed movement
        """
        i_width = self._layer.get_image().get_width()
        i_height = self._layer.get_image().get_height()

        if self.pos_x + i_width <= 0:
            self.pos_x = i_width * speed
            self.pos_y += self._vec_y * speed
        elif (self.pos_x + i_width) > i_width:
            self.pos_x = 0
            self.pos_y += self._vec_y * speed
        if self.pos_y + i_height <= 0:
            self.pos_x += self._vec_x * speed
            self.pos_y += i_height * speed
        elif (self.pos_y + i_height) > i_height:
            self.pos_x += self._vec_x * speed
            self.pos_y += 0
        else:
            self.pos_x += self._vec_x * speed
            self.pos_y += self._vec_y * speed

    def get_layer(self) -> img.GameImage:
        """
        :return: the GameImage layer
        """
        return self._layer
