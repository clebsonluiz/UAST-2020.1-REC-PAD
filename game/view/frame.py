import pygame as pg
import sys


class Frame:

    def __init__(self, width: int, height: int, title: str):
        self.tela = pg.display.set_mode((width, height), pg.HWSURFACE)
        pg.display.set_caption(title)
        pg.display.flip()
        pass

    def get_tela(self) -> pg.Surface:
        return self.tela

    def update(self,):
        pg.display.update()
        pass
