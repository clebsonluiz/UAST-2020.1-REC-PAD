import pygame as pg

from game.constants import *

from ..map import BackgroundMap
from .entity_player import EntityPlayer


class Player:
    """
    Player class, represents the one object player
    that composed of a player and his shadow

    Parameters
    __________
    background: BackgroundMap
        Colision map of this object to the checks his position in screen
    """
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
        """
        :return: bool value, true if this object as ready to be rendenized in screen
        """
        return self.player.loaded() and self.shadow.loaded()

    def do_change_gravit(self):
        """
        change the gravity of the player and the shadow, to do his efect of a mirror
        animations. This call change the gravity and the positions of player and his shadow
        at screen
        """
        self.player.change_gravit()
        self.shadow.change_gravit()
        player_position: tuple = self.player.get_position()
        shadow_position: tuple = self.shadow.get_position()
        self.player.set_position(shadow_position)
        self.shadow.set_position(player_position)

    def do_jump(self):
        """
        this call makes the player and his shadow execute the jump ant screen
        """
        self.player.do_jump()
        self.shadow.do_jump()

    def update(self):
        """
        Updates the current stats of player and his shadow
        """
        self.player.update()
        self.shadow.update()

    def render(self, tela: pg.Surface):
        """
        Render the player and his shadow at screen Surface,

        :param tela: Surface screen frame
        """
        if tela is None or not self.loaded():
            return
        self.shadow.render(tela=tela, color=DARK_GRAY, opacity=200)
        self.player.render(tela=tela)

    def make_animations_list(self):
        """
        build the animations of shadow and player
        """
        self.player.make_animations_list()
        self.shadow.make_animations_list()
