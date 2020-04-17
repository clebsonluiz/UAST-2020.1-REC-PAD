import pygame as pg


class GameImage:
    """
    Image Class used to provide some standard properties for a single image file,
    taking into account the massive use of standard method calls

    """
    def __init__(self, file: str = None):
        if file is not None:
            self._image: pg.Surface = pg.image.load(file)
        else:
            self._image: pg.Surface = pg.Surface()

    def get_image(self) -> pg.Surface:
        return self._image

    def get_especifc_frame(self,
                           x: int = 0, y: int = 0,
                           width: int = 0, height: int = 0,
                           invert_x: bool = False, invert_y: bool = False) -> pg.Surface:
        """
        :param x: x position where the image is located
        :param y: y position where the image is located
        :param width: image width
        :param height: image height
        :param invert_x: if x axis is inverted
        :param invert_y: if y axis is inverted
        :return: Surface image
        """
        from game.constants import BLACK
        image = pg.Surface([width, height]).convert()
        image.set_colorkey(BLACK)
        image.blit(self._image, (0, 0), (x, y, width, height))
        image = pg.transform.flip(image, invert_x, invert_y)
        return image

    def flip(self, invert_x: bool = False, invert_y: bool = False) -> pg.Surface:
        """
        :param invert_x: x axis
        :param invert_y: y axis
        :return: image flipped
        """
        return pg.transform.flip(self._image, invert_x, invert_y)

    @staticmethod
    def from_pygame_surface(file: pg.Surface):
        """
        :param file: pygame Surface
        :return: returns a GameImage from surface
        """
        gi = GameImage(file=None)
        gi._image = file
        return gi
