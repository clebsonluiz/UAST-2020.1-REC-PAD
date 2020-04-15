import pygame as pg

from game.model.entity_player import EntityPlayer
from game.model.map import BackgroundMap
from game.constants import *

class Player:

    def __init__(self, background: BackgroundMap):

        self.player = EntityPlayer(background, )
        self.shadow = EntityPlayer(background, invert_gravity=True)

        self.make_animations_list()

        self.player.pos_x = 40
        self.player.pos_y = background.get_background_rect().centery
        self.shadow.pos_x = self.player.pos_x
        self.shadow.pos_y = self.player.pos_y - self.player.current_sprite().get_height()

        self.player.curr_height = 40
        self.player.curr_width = 50
        self.shadow.curr_height = self.player.curr_height
        self.shadow.curr_width = self.player.curr_width

    def loaded(self) -> bool:
        return self.player.loaded() and self.shadow.loaded()

    def do_change_gravit(self):
        self.player.change_gravit()
        self.shadow.change_gravit()
        player_position: tuple = self.player.get_position()
        shadow_position: tuple = self.shadow.get_position()
        self.player.set_position(shadow_position)
        self.shadow.set_position(player_position)

    def do_jump(self):
        self.player.do_jump()
        self.shadow.do_jump()

    def update(self):
        self.player.update()
        self.shadow.update()

    def render(self, tela: pg.Surface):
        if tela is None:
            return
        self.shadow.render(tela=tela, color=DARK_GRAY, opacity=200)
        self.player.render(tela=tela)

    def make_animations_list(self):
        self.player.make_animations_list()
        self.shadow.make_animations_list()
