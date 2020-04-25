import pygame as pg

from game.constants import *

from ..layer import BackgroundMap
from .entity_player import EntityPlayer


class Player:
    """
    Player class, represents the one object player
    that composed of a player and his shadow

    Parameters
    __________
    background: BackgroundMap
        Colision layer of this object to the checks his position in screen
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
        self.player.set_colision_padding(
            pg.Rect(-20, 0, 45, 0)
        )
        self.shadow.set_colision_padding(
            pg.Rect(-20, 0, 45, 0)
        )

        self._player_score: int = 0

    def increment_score(self):
        """Increments the score of player"""
        self._player_score += 1

    def get_score(self) -> int:
        """
        :return: gets the score of player
        """
        return self._player_score

    def decrement_score(self):
        """Decrements the score of player"""
        self._player_score -= 1

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

        # pg.draw.ellipse(tela, WHITE, self.player.to_rect(), 0, )
        # tela.fill((255, 255, 255), self.player.to_rect())
        self.shadow.render(tela=tela, color=DARK_GRAY, opacity=200)
        self.player.render(tela=tela)

    def to_rect(self) -> pg.Rect:
        """
        :return: the player pg.Rect colision
        """
        return self.player.to_rect()

    def make_animations_list(self):
        """
        build the animations of shadow and player
        """
        self.player.make_animations_list()
        self.shadow.make_animations_list()
