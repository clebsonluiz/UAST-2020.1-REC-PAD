import pygame as pg

from ..layer import BackgroundMap
from ..entity import EntityMap


class EntityPlayer(EntityMap):
    """
    Class of a entity player that will be rendenized in screen.
    this object as will be a shadow of player or a player.
    Shadow and player will realize the same animations but mirrozed.
    Inspired by (Java tutorial Game from ForeignGuyMike)
    """
    def __init__(self, background: BackgroundMap, invert_gravity: bool = False):
        super().__init__('MS6_Hunter_Walker(Edited).png',
                         background=background,
                         invert_gravity=invert_gravity,
                         invert_x=True, )

    def get_animation_row(self) -> int:
        """
        :return: int value of a animation to be executed in event check
        """
        if self.is_jumping():
            return 1
        elif self.is_falling():
            return 2
        return 0

    def make_animations_list(self):
        """
        build the list of animations of this entity
        """
        s_matrix_walking = self.build(
            t_width=63, t_height=39,
            cols=11, rows=1,
            i_x=10, i_y=240,
            jmp_p_x=2, jmp_p_y=0
        )
        s_matrix_jumping_falling = self.build(
            t_width=49, t_height=46,
            cols=9, rows=2,
            i_x=3, i_y=94,
            jmp_p_x=0, jmp_p_y=18
        )
        s_list_walking = EntityMap.sprite_list(
            from_list=s_matrix_walking,
            from_row=0, from_i=0, to_i=11,
        )
        s_list_jumping = EntityMap.sprite_list(
            from_list=s_matrix_jumping_falling,
            from_row=0, from_i=0, to_i=9,
        )
        s_list_falling = EntityMap.sprite_list(
            from_list=s_matrix_jumping_falling,
            from_row=0, from_i=9, to_i=18,
        )

        self.insert(s_list_walking)
        self.insert(s_list_jumping, False)
        self.insert(s_list_falling, False)
        self._loaded = True
