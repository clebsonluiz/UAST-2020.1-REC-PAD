from ..entity import EntityMap
from ...constants import YELLOW, get_render_type

import pygame as pg


class Coin(EntityMap):

    def __init__(self, is_on_top: bool = False):
        super().__init__('from_OpenGameArt_CoinsByPuddin.png',)
        self._loaded: bool = False
        self._is_on_top: bool = is_on_top
        self.make_animations_list()

    def loaded(self) -> bool:
        return self._loaded

    def set_position_on_rect_obstacle(self, obstacle):
        self.pos_x = obstacle.to_rect().centerx - self.to_rect().width / 2
        if self._is_on_top:
            self.pos_y = obstacle.to_rect().bottom + self.to_rect().height / 2
        else:
            self.pos_y = obstacle.to_rect().top - self.to_rect().height * 1.5

    def _get_animation_row(self, is_on_top: bool):
        return 0

    def update(self):
        self.set_curr_row(curr_row=self._get_animation_row(
            is_on_top=self._is_on_top,
        ))
        self.pos_x += self.get_dx()
        self.pos_y += self.get_dy()
        super().update()

    def render(self, tela: pg.Surface):
        """
        render this object at screen frame (tela)

        :param tela: Surface of screen that object will be drawed
        """
        if tela is None:
            return
        if get_render_type().get('COLISION'):
            tela.fill(YELLOW, self.to_rect())
        if get_render_type().get('NORMAL'):
            tela.blit(self.current_sprite(), self.get_position())

    def make_animations_list(self):
        """
        build the list of animations of this entity
        """
        coins = self.build(
            t_width=16, t_height=16,
            cols=8, rows=1,
            i_x=0, i_y=0,
            jmp_p_x=0, jmp_p_y=0,
        )
        s_list_coins = EntityMap.sprite_list(
            from_list=coins,
            from_row=0, from_i=0, to_i=8,
        )
        self.insert(s_list_coins)
        self._loaded = True
